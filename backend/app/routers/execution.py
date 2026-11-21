from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
import json

from app.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission, UserProblemStatus
from app.models.activity import ActivityLog, UserStreak
from app.services.activity_service import record_user_activity
from app.schemas.problem import CodeRunRequest, CodeSubmitRequest, CodeRunResponse, TestCaseResult
from app.services.execution_service import ExecutionService
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/execution", tags=["Code Execution"])

@router.post("/run", response_model=CodeRunResponse)
def run_code(
    req: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If custom input is provided, run only for that input
    if req.custom_input is not None and req.custom_input != "":
        test_cases = [{"input": req.custom_input, "expected_output": ""}]
    elif req.problem_id:
        prob = db.query(Problem).filter(Problem.id == req.problem_id).first()
        if not prob:
            raise HTTPException(status_code=404, detail="Problem not found")
        test_cases = json.loads(prob.sample_test_cases)
    else:
        test_cases = [{"input": "", "expected_output": ""}]

    exec_result = ExecutionService.run_isolated(
        language=req.language,
        code=req.code,
        test_cases=test_cases,
        timeout_seconds=3.0
    )

    ai_feedback = None
    if exec_result["status"] != "Accepted" and exec_result["status"] != "Success":
        # Get instant intelligent debug hint
        dbg = AIService.analyze_code_for_debugging(
            language=req.language,
            code=req.code,
            runtime_error=exec_result.get("stderr"),
            failed_test_case=exec_result["test_results"][0] if exec_result["test_results"] else None
        )
        ai_feedback = f"{dbg['summary']}: {dbg['how_to_fix']}"

    return CodeRunResponse(
        status=exec_result["status"],
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        runtime_ms=exec_result["runtime_ms"],
        passed_tests=exec_result["passed_tests"],
        total_tests=exec_result["total_tests"],
        test_results=[
            TestCaseResult(
                test_case_id=tr["test_case_id"],
                input=str(tr["input"]),
                expected_output=str(tr["expected_output"]),
                actual_output=str(tr["actual_output"]),
                passed=tr["passed"],
                error=tr.get("error"),
                runtime_ms=tr.get("runtime_ms", 0.0)
            )
            for tr in exec_result["test_results"]
        ],
        ai_feedback=ai_feedback
    )

@router.post("/submit", response_model=CodeRunResponse)
def submit_code(
    req: CodeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prob = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    sample_tests = json.loads(prob.sample_test_cases)
    hidden_tests = json.loads(prob.hidden_test_cases)
    all_tests = sample_tests + hidden_tests

    exec_result = ExecutionService.run_isolated(
        language=req.language,
        code=req.code,
        test_cases=all_tests,
        timeout_seconds=4.0
    )

    # Intelligent Debugger explanation
    ai_feedback = None
    if exec_result["status"] != "Accepted":
        failed_tc = next((t for t in exec_result["test_results"] if not t["passed"]), None)
        dbg = AIService.analyze_code_for_debugging(
            language=req.language,
            code=req.code,
            problem_description=prob.description,
            runtime_error=exec_result.get("stderr"),
            failed_test_case=failed_tc
        )
        ai_feedback = f"{dbg['error_type']}: {dbg['why_it_happened']}\n\nDirection: {dbg['how_to_fix']}"

    # Persist Submission
    sub = Submission(
        user_id=current_user.id,
        problem_id=prob.id,
        language=req.language,
        code=req.code,
        status=exec_result["status"],
        runtime_ms=exec_result["runtime_ms"],
        passed_tests=exec_result["passed_tests"],
        total_tests=exec_result["total_tests"],
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        ai_debug_feedback=ai_feedback
    )
    db.add(sub)

    # Update UserProblemStatus
    status_rec = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.problem_id == prob.id
    ).first()

    now = datetime.utcnow()
    is_accepted = (exec_result["status"] == "Accepted")

    if not status_rec:
        status_rec = UserProblemStatus(
            user_id=current_user.id,
            problem_id=prob.id,
            status="Solved" if is_accepted else "Attempted",
            last_attempted_at=now,
            solved_at=now if is_accepted else None
        )
        db.add(status_rec)
    else:
        status_rec.last_attempted_at = now
        if is_accepted:
            status_rec.status = "Solved"
            if not status_rec.solved_at:
                status_rec.solved_at = now
        elif status_rec.status != "Solved":
            status_rec.status = "Attempted"

    # Log meaningful activity and update streaks via centralized service
    record_user_activity(
        db=db,
        user_id=current_user.id,
        action_type="problem_solved" if is_accepted else "submission_attempt",
        topic=prob.topic,
        metadata_json={"slug": prob.slug, "status": exec_result["status"]},
        active_seconds=300
    )

    return CodeRunResponse(
        status=exec_result["status"],
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        runtime_ms=exec_result["runtime_ms"],
        passed_tests=exec_result["passed_tests"],
        total_tests=exec_result["total_tests"],
        test_results=[
            TestCaseResult(
                test_case_id=tr["test_case_id"],
                input=str(tr["input"]),
                expected_output=str(tr["expected_output"]),
                actual_output=str(tr["actual_output"]),
                passed=tr["passed"],
                error=tr.get("error"),
                runtime_ms=tr.get("runtime_ms", 0.0)
            )
            for tr in exec_result["test_results"]
        ],
        ai_feedback=ai_feedback
    )
