from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    topic = Column(String(100), nullable=False) # Arrays, Strings, Trees, Graphs, DP, etc.
    subtopic = Column(String(100), default="General")
    algorithmic_pattern = Column(String(100), default="Standard") # Two Pointers, Sliding Window, BFS, DFS, Memoization, etc.
    difficulty = Column(String(20), default="Medium") # Easy, Medium, Hard
    
    description = Column(Text, nullable=False)
    constraints = Column(Text, nullable=False)
    input_format = Column(Text, nullable=False)
    output_format = Column(Text, nullable=False)
    
    # JSON strings
    examples_json = Column(Text, nullable=False) # [{"input": "...", "output": "...", "explanation": "..."}]
    sample_test_cases = Column(Text, nullable=False) # [{"input": "...", "expected_output": "..."}]
    hidden_test_cases = Column(Text, nullable=False) # [{"input": "...", "expected_output": "..."}]
    
    # Starter code
    starter_code_python = Column(Text, nullable=False)
    starter_code_java = Column(Text, nullable=False)
    
    # 3-Level Progressive Hint System
    hint_level_1 = Column(Text, nullable=False) # Conceptual clue
    hint_level_2 = Column(Text, nullable=False) # Algorithmic direction
    hint_level_3 = Column(Text, nullable=False) # Pseudocode structure
    
    expected_time_complexity = Column(String(50), default="O(n)")
    expected_space_complexity = Column(String(50), default="O(1)")
    
    created_at = Column(DateTime, default=datetime.utcnow)
