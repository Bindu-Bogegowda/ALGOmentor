from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from datetime import datetime, date
from app.database import Base

class DailyPerformanceReview(Base):
    __tablename__ = "daily_performance_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review_date = Column(Date, default=date.today, nullable=False)
    
    # 7 Required Pillars of Daily Review
    overall_summary = Column(Text, nullable=False)
    strengths_json = Column(Text, nullable=False) # JSON list
    common_mistakes_json = Column(Text, nullable=False) # JSON list
    concepts_to_improve_json = Column(Text, nullable=False) # JSON list
    recommended_revisions_json = Column(Text, nullable=False) # JSON list
    next_day_plan_json = Column(Text, nullable=False) # JSON list
    achievable_targets_json = Column(Text, nullable=False) # JSON list
    
    # Quantitative metrics snapshot
    metrics_json = Column(Text, default="{}") # {problems_attempted: 2, problems_solved: 1, accuracy: 50, active_minutes: 45}
    created_at = Column(DateTime, default=datetime.utcnow)
