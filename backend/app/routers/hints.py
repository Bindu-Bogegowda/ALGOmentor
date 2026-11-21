from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import UserProblemStatus, HintUsage
from app.schemas.problem import HintRequest, HintResponse
from app.services.auth_service import get_current_user
from app.services.ai_service import AIService

router = APIRouter(prefix="/hints", tags=["Progressive Hints"])

def _generate_edge_cases_hint(prob: Problem) -> str:
    topic = (prob.topic or "").lower()
    return (
        f"Key Edge Cases & Boundary Conditions for '{prob.title}':\n"
        f"1. Empty or Minimal Input: Test with n = 0, n = 1, or empty collections.\n"
        f"2. Duplicates & Collisions: Check behavior when duplicate values exist in the input array or map.\n"
        f"3. Negative & Extreme Values: Guard against negative values, zeroes, or large values exceeding 32-bit signed integers.\n"
        f"4. Target Absence: If searching or matching, ensure your method handles the case where no valid result exists gracefully.\n"
        f"5. Boundary Invariants: Check 0-based index limits to prevent IndexOutOfBoundsException."
    )

def _generate_code_skeleton_hint(prob: Problem) -> str:
    # Build clean Java skeleton
    starter = prob.starter_code_java or ""
    return (
        f"Java Solution Architecture & Method Skeleton:\n\n"
        f"{starter}\n\n"
        f"/* Step-by-Step Implementation Guide:\n"
        f" * Step 1: Validate input bounds (guard clauses for null or empty).\n"
        f" * Step 2: Initialize auxiliary data structures (e.g. Map, Set, or pointers).\n"
        f" * Step 3: Iterate through elements and maintain invariant state.\n"
        f" * Step 4: Check match conditions and return early where possible.\n"
        f" * Step 5: Return fallback/default result.\n"
        f" */"
    )

def _generate_complexity_hint(prob: Problem) -> str:
    time_target = prob.expected_time_complexity or "O(N)"
    space_target = prob.expected_space_complexity or "O(N)"
    return (
        f"Complexity Bottlenecks & Optimization Roadmap:\n"
        f"• Target Time Complexity: {time_target}\n"
        f"• Target Space Complexity: {space_target}\n\n"
        f"How to optimize from Brute Force:\n"
        f"1. A naive brute-force approach requires nested loops taking O(N^2) time.\n"
        f"2. By spending auxiliary space ({space_target}), you trade memory for speed, allowing O(1) lookups.\n"
        f"3. Avoid repeatedly recomputing values or searching linearly. Store seen values or use two pointers."
    )

@router.post("", response_model=HintResponse)
def get_progressive_hint(
    req: HintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prob = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    level = req.level
    if level < 1:
        raise HTTPException(status_code=400, detail="Hint level must be a positive integer (>= 1)")

    # Record hint usage
    usage = HintUsage(
        user_id=current_user.id,
        problem_id=prob.id,
        hint_level=level
    )
    db.add(usage)

    # Update highest hint level in status
    status_rec = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.problem_id == prob.id
    ).first()
    if status_rec:
        status_rec.highest_hint_level_used = max(status_rec.highest_hint_level_used, level)
    else:
        status_rec = UserProblemStatus(
            user_id=current_user.id,
            problem_id=prob.id,
            highest_hint_level_used=level
        )
        db.add(status_rec)
    db.commit()

    # Unlimited Progressive Hint Hierarchy
    if level == 1:
        return HintResponse(
            level=1,
            title="Level 1: Conceptual Clue",
            content=prob.hint_level_1 or "Think about the problem invariants and which data structure gives fast lookups."
        )
    elif level == 2:
        return HintResponse(
            level=2,
            title="Level 2: Algorithmic Direction",
            content=prob.hint_level_2 or "Consider trading auxiliary space for time by caching previously visited items."
        )
    elif level == 3:
        return HintResponse(
            level=3,
            title="Level 3: Pseudocode Architecture",
            content=prob.hint_level_3 or "Initialize state -> Iterate through collection -> Query lookup map -> Return match."
        )
    elif level == 4:
        return HintResponse(
            level=4,
            title="Level 4: Edge Cases & Boundary Conditions",
            content=_generate_edge_cases_hint(prob)
        )
    elif level == 5:
        return HintResponse(
            level=5,
            title="Level 5: Code Skeleton & Method Signatures (Java)",
            content=_generate_code_skeleton_hint(prob)
        )
    elif level == 6:
        return HintResponse(
            level=6,
            title="Level 6: Complexity Bottleneck & Optimization",
            content=_generate_complexity_hint(prob)
        )
    else:
        # Dynamic AI Hint for Level 7+ tailored to current code
        title = f"Level {level}: Dynamic AI Pedagogical Hint"
        if req.current_code and len(req.current_code.strip()) > 10:
            ai_res = AIService._offline_tutor_response(
                message=f"I am working on problem '{prob.title}' and requested Hint Level {level}. Provide a progressive hint analyzing my current code logic without giving away the complete solution. Point out what variable, pointer, or condition to check next.",
                context_page="practice",
                current_code=req.current_code,
                problem_title=prob.title,
                error_message=None,
                student_level=current_user.difficulty_level or "Beginner"
            )
            content = ai_res.get("reply", "Check your loop termination condition and how pointers advance.")
        else:
            content = (
                f"Progressive Insight for '{prob.title}' (Level {level}):\n\n"
                f"• Invariant Check: At each step of your loop, ask what property is guaranteed to hold true.\n"
                f"• Walkthrough with Sample Input: Trace the first two elements by hand. What values should be in your helper data structure after processing element 0?\n"
                f"• Pro Tip: Type some initial code in the editor and click 'Ask AI Mentor' for code-specific hints!"
            )
        return HintResponse(
            level=level,
            title=title,
            content=content
        )
