"""
Centralized Activity & Streak Tracking Service for AlgoMentor.
Ensures every eligible learning activity (concept completion, code solution,
quiz submission, visualizer run) updates both the ActivityLog and UserStreak tables.
"""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
import json

from app.models.activity import ActivityLog, UserStreak


def record_user_activity(
    db: Session,
    user_id: int,
    action_type: str,
    topic: str = "General",
    metadata_json: dict = None,
    active_seconds: int = 120
) -> ActivityLog:
    """
    Records an atomic learning activity and advances the user's streak.
    Eligible actions:
      - 'lesson_completed': Finished a concept lesson
      - 'problem_solved': Code submission passed all test cases
      - 'submission_attempt': Code submitted
      - 'quiz_completed': Passed concept mastery assessment
      - 'visualization_run': Interactive visualizer step execution
      - 'challenge_completed': Solved a daily/weekly challenge
    """
    # 1. Create the persistent ActivityLog record
    meta_str = json.dumps(metadata_json or {})
    act = ActivityLog(
        user_id=user_id,
        action_type=action_type,
        topic=topic,
        metadata_json=meta_str,
        active_seconds=active_seconds,
        created_at=datetime.utcnow()
    )
    db.add(act)

    # 2. Update or initialize the UserStreak record
    streak_rec = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    today_date = date.today()

    if not streak_rec:
        streak_rec = UserStreak(
            user_id=user_id,
            current_streak=1,
            longest_streak=1,
            last_activity_date=today_date,
            total_active_days=1
        )
        db.add(streak_rec)
    else:
        # Check if already recorded an activity today
        if streak_rec.last_activity_date != today_date:
            yesterday = today_date - timedelta(days=1)
            if streak_rec.last_activity_date == yesterday:
                streak_rec.current_streak += 1
            else:
                streak_rec.current_streak = 1
            
            streak_rec.longest_streak = max(streak_rec.longest_streak, streak_rec.current_streak)
            streak_rec.last_activity_date = today_date
            streak_rec.total_active_days += 1

    db.commit()
    return act
