from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from datetime import datetime
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    language = Column(String(20), default="python") # python, java
    code = Column(Text, nullable=False)
    
    status = Column(String(50), nullable=False) # "Accepted", "Wrong Answer", "Runtime Error", "Time Limit Exceeded"
    runtime_ms = Column(Float, default=0.0)
    memory_mb = Column(Float, default=0.0)
    passed_tests = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    error_message = Column(Text, default="")
    
    # Intelligent Debugger output
    ai_debug_feedback = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProblemStatus(Base):
    __tablename__ = "user_problem_statuses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    
    status = Column(String(20), default="Unsolved") # "Unsolved", "Attempted", "Solved"
    is_bookmarked = Column(Boolean, default=False)
    is_in_revision = Column(Boolean, default=False)
    
    highest_hint_level_used = Column(Integer, default=0) # 0, 1, 2, 3
    last_attempted_at = Column(DateTime, nullable=True)
    solved_at = Column(DateTime, nullable=True)

class HintUsage(Base):
    __tablename__ = "hint_usages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    hint_level = Column(Integer, nullable=False) # 1, 2, 3
    created_at = Column(DateTime, default=datetime.utcnow)
