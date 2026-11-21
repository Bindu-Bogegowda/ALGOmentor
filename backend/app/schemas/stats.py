from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class DailyGoal(BaseModel):
    id: str
    title: str
    target: int
    current: int
    unit: str
    completed: bool

class DashboardStats(BaseModel):
    welcome_message: str
    user_name: str
    user_avatar: str
    current_roadmap: str
    current_level: str
    
    # Core Counters
    concepts_completed: int
    total_concepts: int
    problems_solved: int
    problems_attempted: int
    total_problems: int
    
    # Streaks & Mastery
    current_streak: int
    longest_streak: int
    weekly_learning_hours: float
    mastery_percentage: float
    
    # Goals & Reviews
    daily_goals: List[DailyGoal]
    recent_activities: List[Dict[str, Any]]
    recommended_lessons: List[Dict[str, Any]]
    quick_review_snippet: Optional[Dict[str, Any]] = None

class StreakDay(BaseModel):
    date: str
    count: int
    level: int # 0 to 4
    details: Optional[Dict[str, int]] = None

class MonthlyActivity(BaseModel):
    month_name: str # e.g. "Nov 2026"
    month_key: str  # e.g. "2026-11"
    activity_count: int
    active_days: int

class ActivityLogCreate(BaseModel):
    action_type: str # "visualization_run", "lesson_completed", "problem_solved", "quiz_completed"
    topic: str = "General"
    active_seconds: int = 120
    metadata: Optional[Dict[str, Any]] = None

class StreakCalendarResponse(BaseModel):
    current_streak: int
    longest_streak: int
    total_active_days: int
    total_problems_solved: int = 0
    total_activities_year: int = 0
    calendar_days: List[StreakDay]
    monthly_history: List[MonthlyActivity] = []
    weekly_stats: Optional[Dict[str, Any]] = None

class WeeklyDayMetric(BaseModel):
    day: str # Mon, Tue, etc.
    concept_hours: float
    coding_hours: float
    visualizer_hours: float
    problems_solved: int

class WeeklyAnalyticsResponse(BaseModel):
    total_weekly_hours: float
    active_days_count: int
    coding_time_pct: float
    concept_time_pct: float
    daily_breakdown: List[WeeklyDayMetric]
    topic_distribution: List[Dict[str, Any]]
    trend_comparison: str

class DailyReviewResponse(BaseModel):
    review_date: str
    overall_summary: str
    strengths: List[str]
    common_mistakes: List[str]
    concepts_to_improve: List[str]
    recommended_revisions: List[str]
    next_day_plan: List[str]
    achievable_targets: List[str]
    metrics: Dict[str, Any]
