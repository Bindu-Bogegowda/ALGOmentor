from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(100), primary_key=True) # e.g. "lesson_bubble_sort"
    topic_id = Column(String(100), ForeignKey("roadmap_topics.id"), nullable=False)
    category = Column(String(50), default="dsa") # e.g. "Arrays", "Dynamic Programming", etc.
    difficulty = Column(String(30), default="Beginner") # "Beginner", "Intermediate", "Advanced"
    title = Column(String(200), nullable=False)
    summary = Column(Text, nullable=False)
    
    # Detailed Educational Fields
    fundamental_explanation = Column(Text, nullable=False)
    step_by_step = Column(Text, nullable=False) # JSON string or markdown steps
    real_world_applications = Column(Text, nullable=False)
    examples_illustrations = Column(Text, nullable=False)
    pseudocode = Column(Text, nullable=False)
    time_complexity = Column(String(100), default="O(n)")
    space_complexity = Column(String(100), default="O(1)")
    prerequisites = Column(String(255), default="Basic programming logic")
    related_concepts = Column(String(255), default="")
    
    # Video Lesson Reference
    video_url = Column(String(500), default="https://www.youtube.com/embed/kPRA0W1kECg")
    video_title = Column(String(255), default="Algorithm Walkthrough")
    
    # Visualization link
    visualization_type = Column(String(50), nullable=True) # "sorting", "searching", "linked_list", "stack_queue", "tree", "graph", "dijkstra", "dp"
    visualization_algorithm = Column(String(50), nullable=True) # "bubble_sort", "binary_search", "bfs", "dfs", "dijkstra", etc.
    
    practice_problem_slug = Column(String(100), nullable=True)
    order_index = Column(Integer, default=0)
    step_number = Column(Integer, default=1)
    stage_name = Column(String(100), default="Core Foundations")
    level_number = Column(Integer, default=1)
    level_title = Column(String(100), default="Level 1: Programming Foundations")
    
    # 18-Part Learning Architecture Fields
    why_learn_it = Column(Text, default="")
    core_theory = Column(Text, default="")
    dry_run = Column(Text, default="[]") # JSON list of execution steps with variable snapshots
    java_code = Column(Text, default="") # Java implementation with annotations
    python_code = Column(Text, default="") # Python implementation with annotations
    practice_questions = Column(Text, default="[]") # JSON list of questions {difficulty, title, description, constraints}
    ai_hints = Column(Text, default="[]") # JSON list of 3 progressive hints {level, title, hint}
    common_mistakes = Column(Text, default="") # Frequent student errors and pitfalls
    concept_connections = Column(Text, default="{}") # JSON object of prerequisites, related, next concepts
    quiz_questions = Column(Text, default="[]") # JSON list of quiz questions {id, question, options, correct_idx, explanation}
    mastery_threshold = Column(Integer, default=70) # Required percentage to master

    prev_lesson_id = Column(String(100), nullable=True)
    next_lesson_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(100), ForeignKey("lessons.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    quiz_score = Column(Integer, default=0)
    mastery_level = Column(String(50), default="not_started") # "not_started", "learning", "proficient", "mastered"
