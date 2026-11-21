from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class LessonSummary(BaseModel):
    id: str
    topic_id: str
    category: str = "dsa"
    difficulty: str = "Beginner"
    prerequisites: Optional[str] = "None"
    title: str
    summary: str
    time_complexity: str
    space_complexity: str
    visualization_type: Optional[str] = None
    visualization_algorithm: Optional[str] = None
    is_completed: bool = False
    mastery_level: str = "not_started"
    quiz_score: int = 0
    order_index: int = 0
    step_number: int = 1
    stage_name: str = "Core Foundations"
    level_number: int = 1
    level_title: str = "Level 1: Programming Foundations"
    prev_lesson_id: Optional[str] = None
    next_lesson_id: Optional[str] = None

class LessonDetail(LessonSummary):
    fundamental_explanation: str
    step_by_step: str
    real_world_applications: str
    examples_illustrations: str
    pseudocode: str
    prerequisites: str
    related_concepts: str
    video_url: str
    video_title: str
    practice_problem_slug: Optional[str] = None
    prev_lesson_title: Optional[str] = None
    next_lesson_title: Optional[str] = None
    
    # 18-Part Educational Structure
    why_learn_it: str = ""
    core_theory: str = ""
    dry_run: str = "[]"
    java_code: str = ""
    python_code: str = ""
    practice_questions: str = "[]"
    ai_hints: str = "[]"
    common_mistakes: str = ""
    concept_connections: str = "{}"
    quiz_questions: str = "[]"
    mastery_threshold: int = 70

class LessonProgressUpdate(BaseModel):
    is_completed: bool
    time_spent_seconds: int = 60

class LessonQuizSubmit(BaseModel):
    answers: Dict[str, int] # question_idx string -> selected_option_idx

class LessonQuizResult(BaseModel):
    score_percent: int
    correct_count: int
    total_questions: int
    is_passed: bool
    mastery_level: str
    feedback: str
    unlocked_next_lesson_id: Optional[str] = None

class DependencyGraphNode(BaseModel):
    id: str
    title: str
    level_number: int
    level_title: str
    category: str
    difficulty: str = "Beginner"
    is_completed: bool
    mastery_level: str
    step_number: int

class DependencyGraphEdge(BaseModel):
    source: str
    target: str
    type: str = "prerequisite" # "prerequisite" or "next_step"

class DependencyGraphResponse(BaseModel):
    nodes: List[DependencyGraphNode]
    edges: List[DependencyGraphEdge]
