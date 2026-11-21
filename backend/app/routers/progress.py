from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models.user import User
from app.models.lesson import Lesson, UserLessonProgress
from app.models.problem import Problem
from app.models.submission import Submission, UserProblemStatus
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress & Mastery Tracker"])

@router.get("/mastery")
def get_mastery_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Total concepts
    total_concepts = db.query(Lesson).count()
    completed_concepts = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.is_completed == True
    ).count()

    # Problems
    total_problems = db.query(Problem).count()
    solved_problems = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.status == "Solved"
    ).count()
    attempted_problems = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.status == "Attempted"
    ).count()
    unsolved_problems = max(0, total_problems - solved_problems - attempted_problems)

    # Topic-wise mastery breakdown
    topics = db.query(Problem.topic).distinct().all()
    topic_breakdown = []
    for (t_name,) in topics:
        t_total = db.query(Problem).filter(Problem.topic == t_name).count()
        t_solved = db.query(UserProblemStatus).join(Problem).filter(
            UserProblemStatus.user_id == current_user.id,
            Problem.topic == t_name,
            UserProblemStatus.status == "Solved"
        ).count()
        t_pct = round((t_solved / max(1, t_total)) * 100, 1)
        topic_breakdown.append({
            "topic": t_name,
            "solved": t_solved,
            "total": t_total,
            "percentage": t_pct
        })

    # Submissions accuracy
    total_subs = db.query(Submission).filter(Submission.user_id == current_user.id).count()
    accepted_subs = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.status == "Accepted"
    ).count()
    accuracy = round((accepted_subs / max(1, total_subs)) * 100, 1) if total_subs > 0 else 100.0

    return {
        "total_concepts": total_concepts,
        "completed_concepts": completed_concepts,
        "concept_completion_pct": round((completed_concepts / max(1, total_concepts)) * 100, 1),
        "total_problems": total_problems,
        "solved_problems": solved_problems,
        "attempted_problems": attempted_problems,
        "unsolved_problems": unsolved_problems,
        "total_submissions": total_subs,
        "accuracy_pct": accuracy,
        "topic_breakdown": topic_breakdown,
        "learning_consistency": "High" if solved_problems >= 2 else "Moderate"
    }
