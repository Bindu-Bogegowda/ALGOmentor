from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from datetime import datetime
from app.database import Base

class RoadmapStream(Base):
    __tablename__ = "roadmap_streams"

    id = Column(String(50), primary_key=True) # e.g. "dsa", "aiml", "dl", "daa", "graph", "optimization", "computational"
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), default="core")
    icon = Column(String(50), default="Network")
    order_index = Column(Integer, default=0)
    total_hours_estimate = Column(Integer, default=40)
    prerequisites = Column(Text, default="None")
    created_at = Column(DateTime, default=datetime.utcnow)

class RoadmapTopic(Base):
    __tablename__ = "roadmap_topics"

    id = Column(String(100), primary_key=True) # e.g. "dsa_arrays_101"
    stream_id = Column(String(50), ForeignKey("roadmap_streams.id"), nullable=False)
    title = Column(String(150), nullable=False)
    level = Column(String(20), default="Beginner") # Beginner, Intermediate, Advanced, Master
    description = Column(Text, nullable=False)
    estimated_minutes = Column(Integer, default=60)
    order_index = Column(Integer, default=0)
    prerequisite_topic_id = Column(String(100), nullable=True)
    milestone_tag = Column(String(100), default="Foundational")
    created_at = Column(DateTime, default=datetime.utcnow)

class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(String(100), ForeignKey("roadmap_topics.id"), nullable=False)
    is_unlocked = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
