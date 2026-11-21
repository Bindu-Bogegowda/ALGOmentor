from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from datetime import datetime, date
from app.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String(50), nullable=False) # "problem_solved", "submission_attempt", "lesson_completed", "visualization_run", "project_saved"
    topic = Column(String(100), default="General")
    metadata_json = Column(Text, default="{}")
    active_seconds = Column(Integer, default=120) # active time tracked for this action
    created_at = Column(DateTime, default=datetime.utcnow)

class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    total_active_days = Column(Integer, default=0)
