from pydantic import BaseModel
from typing import List, Optional

class RoadmapTopicItem(BaseModel):
    id: str
    stream_id: str
    title: str
    level: str
    description: str
    estimated_minutes: int
    order_index: int
    prerequisite_topic_id: Optional[str] = None
    milestone_tag: str
    is_unlocked: bool = True
    is_completed: bool = False
    progress_percentage: float = 0.0

class RoadmapStreamDetail(BaseModel):
    id: str
    title: str
    description: str
    category: str
    icon: str
    total_hours_estimate: int
    prerequisites: str
    topics: List[RoadmapTopicItem] = []
    user_completion_pct: float = 0.0
