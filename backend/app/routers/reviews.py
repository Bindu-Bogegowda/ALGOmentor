from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
import json

from app.database import get_db
from app.models.user import User
from app.models.review import DailyPerformanceReview
from app.schemas.stats import DailyReviewResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/reviews", tags=["Daily Performance Review"])

@router.get("/today", response_model=DailyReviewResponse)
def get_daily_review(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = date.today()
    rev = db.query(DailyPerformanceReview).filter(
        DailyPerformanceReview.user_id == current_user.id
    ).order_by(DailyPerformanceReview.created_at.desc()).first()

    if not rev:
        # Default report for initial profile
        return DailyReviewResponse(
            review_date=str(today),
            overall_summary="Welcome to AlgoMentor! Your learning telemetry is initialized and tracking every code execution, algorithm visualization step, and concept milestone.",
            strengths=[
                "Initialized personalized algorithm roadmap.",
                "Explored foundational data structures.",
                "Enthusiastic start with active problem solving."
            ],
            common_mistakes=[
                "Off-by-one boundary conditions in index loops.",
                "Omitting edge cases for empty or single-element inputs."
            ],
            concepts_to_improve=[
                "Hash Map lookup patterns for O(N) optimizations.",
                "Recursion tree diagrams for Divide & Conquer."
            ],
            recommended_revisions=[
                "Bubble Sort invariants and swap termination.",
                "Binary Search pointer updates."
            ],
            next_day_plan=[
                "Solve 1 Easy string manipulation problem.",
                "Step through the Interactive Binary Search visualizer.",
                "Complete the Linked List pointers concept lesson."
            ],
            achievable_targets=[
                "Earn first accepted submission on Two Sum.",
                "Achieve 2-day activity streak.",
                "Complete 1 interactive visualizer step run."
            ],
            metrics={"problems_attempted": 0, "problems_solved": 0, "accuracy": 100.0, "active_minutes": 15}
        )

    return DailyReviewResponse(
        review_date=str(rev.review_date),
        overall_summary=rev.overall_summary,
        strengths=json.loads(rev.strengths_json),
        common_mistakes=json.loads(rev.common_mistakes_json),
        concepts_to_improve=json.loads(rev.concepts_to_improve_json),
        recommended_revisions=json.loads(rev.recommended_revisions_json),
        next_day_plan=json.loads(rev.next_day_plan_json),
        achievable_targets=json.loads(rev.achievable_targets_json),
        metrics=json.loads(rev.metrics_json or "{}")
    )
