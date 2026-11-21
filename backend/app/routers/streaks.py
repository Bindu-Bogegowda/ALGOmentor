from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict

from app.database import get_db
from app.models.user import User
from app.models.activity import ActivityLog, UserStreak
from app.models.submission import UserProblemStatus
from app.schemas.stats import StreakCalendarResponse, StreakDay, MonthlyActivity, ActivityLogCreate
from app.services.auth_service import get_current_user
from app.services.activity_service import record_user_activity

router = APIRouter(prefix="/streaks", tags=["Activity & Streaks"])

@router.get("/calendar", response_model=StreakCalendarResponse)
def get_streak_calendar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Computes a full 365-day GitHub / LeetCode style activity heatmap for the student.
    Calculates consecutive streaks, activity types per day, and month-by-month history.
    """
    today = date.today()
    one_year_ago = today - timedelta(days=364)

    # 1. Fetch all user activities for the past 365 days
    logs = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(ActivityLog.created_at.asc()).all()

    # Aggregate by date and action_type
    date_action_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    all_active_dates = set()

    for l in logs:
        d_str = l.created_at.strftime("%Y-%m-%d")
        all_active_dates.add(d_str)
        date_action_counts[d_str]["total"] += 1
        date_action_counts[d_str][l.action_type] += 1

    # 2. Build 365 days calendar list
    calendar_days: List[StreakDay] = []
    total_activities_year = 0

    for i in range(364, -1, -1):
        day_date = today - timedelta(days=i)
        d_str = day_date.strftime("%Y-%m-%d")
        day_info = date_action_counts.get(d_str, {})
        cnt = day_info.get("total", 0)
        total_activities_year += cnt

        # Determine green contribution level (0 to 4)
        if cnt == 0:
            lvl = 0
        elif cnt == 1:
            lvl = 1 # Light green
        elif cnt <= 3:
            lvl = 2 # Medium green
        elif cnt <= 5:
            lvl = 3 # Green
        else:
            lvl = 4 # Dark green

        details = {
            "problems_solved": day_info.get("problem_solved", 0),
            "concepts_completed": day_info.get("lesson_completed", 0),
            "quizzes_passed": day_info.get("quiz_completed", 0),
            "visualizations_run": day_info.get("visualization_run", 0),
            "other_activities": sum(v for k, v in day_info.items() if k not in ["total", "problem_solved", "lesson_completed", "quiz_completed", "visualization_run"])
        }

        calendar_days.append(StreakDay(
            date=d_str,
            count=cnt,
            level=lvl,
            details=details
        ))

    # 3. Dynamic Consecutive Streak Calculation from real activity calendar
    sorted_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in all_active_dates])
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    prev_date = None

    for d in sorted_dates:
        if prev_date is None:
            temp_streak = 1
        elif d == prev_date + timedelta(days=1):
            temp_streak += 1
        elif d > prev_date + timedelta(days=1):
            temp_streak = 1
        longest_streak = max(longest_streak, temp_streak)
        prev_date = d

    # Calculate active current streak leading up to today or yesterday
    yesterday = today - timedelta(days=1)
    if today in sorted_dates or yesterday in sorted_dates:
        check_date = today if today in sorted_dates else yesterday
        while check_date in sorted_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
    else:
        current_streak = 0

    # Fallback to UserStreak record if available and higher
    streak_rec = db.query(UserStreak).filter(UserStreak.user_id == current_user.id).first()
    if streak_rec:
        current_streak = max(current_streak, streak_rec.current_streak)
        longest_streak = max(longest_streak, streak_rec.longest_streak)
        total_active_days = max(len(all_active_dates), streak_rec.total_active_days)
    else:
        total_active_days = len(all_active_dates)

    # 4. Total problems solved count
    total_problems_solved = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.status == "Solved"
    ).count()

    # 5. Month-by-month activity history (past 12 months)
    monthly_data: Dict[str, Dict[str, Any]] = {}
    for i in range(11, -1, -1):
        m_start = (today.replace(day=1) - timedelta(days=i * 28)).replace(day=1)
        m_key = m_start.strftime("%Y-%m")
        m_name = m_start.strftime("%b %Y")
        monthly_data[m_key] = {
            "month_name": m_name,
            "month_key": m_key,
            "activity_count": 0,
            "active_days": set()
        }

    for d_str, day_info in date_action_counts.items():
        m_key = d_str[:7]
        if m_key in monthly_data:
            monthly_data[m_key]["activity_count"] += day_info.get("total", 0)
            if day_info.get("total", 0) > 0:
                monthly_data[m_key]["active_days"].add(d_str)

    monthly_history = [
        MonthlyActivity(
            month_name=v["month_name"],
            month_key=v["month_key"],
            activity_count=v["activity_count"],
            active_days=len(v["active_days"])
        )
        for v in monthly_data.values()
    ]

    # 6. Weekly statistics (past 7 days)
    seven_days_ago = today - timedelta(days=6)
    week_activities = sum(
        date_action_counts.get((seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d"), {}).get("total", 0)
        for i in range(7)
    )
    week_active_days = sum(
        1 for i in range(7)
        if date_action_counts.get((seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d"), {}).get("total", 0) > 0
    )

    weekly_stats = {
        "this_week_activities": week_activities,
        "this_week_active_days": week_active_days,
        "completion_rate": round((week_active_days / 7.0) * 100, 1)
    }

    return StreakCalendarResponse(
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_active_days=total_active_days,
        total_problems_solved=total_problems_solved,
        total_activities_year=total_activities_year,
        calendar_days=calendar_days,
        monthly_history=monthly_history,
        weekly_stats=weekly_stats
    )

@router.post("/log-activity")
def log_student_activity(
    body: ActivityLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Explicit endpoint to record activities (e.g. from visualizer lessons or challenge runs).
    """
    act = record_user_activity(
        db=db,
        user_id=current_user.id,
        action_type=body.action_type,
        topic=body.topic,
        metadata_json=body.metadata,
        active_seconds=body.active_seconds
    )
    return {"status": "success", "activity_id": act.id}
