from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), default="Algorithm Explorer")
    avatar = Column(String(255), default="https://api.dicebear.com/7.x/bottts/svg?seed=algomentor")
    bio = Column(Text, default="Passionate about algorithms, logic structures and problem solving.")
    
    # Preferences & Progress
    preferred_language = Column(String(20), default="python") # python, java
    difficulty_level = Column(String(20), default="Beginner") # Beginner, Intermediate, Advanced, Master
    active_roadmap = Column(String(50), default="dsa") # dsa, aiml, dl, daa, graph, optimization, computational
    theme = Column(String(10), default="dark") # dark, light
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
