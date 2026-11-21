from pydantic import BaseModel
from typing import Optional, List, Any

class ProblemSummary(BaseModel):
    id: int
    slug: str
    title: str
    topic: str
    subtopic: str
    algorithmic_pattern: str
    difficulty: str
    expected_time_complexity: str
    expected_space_complexity: str
    status: str = "Unsolved" # Unsolved, Attempted, Solved
    is_bookmarked: bool = False
    is_in_revision: bool = False

class ProblemDetail(ProblemSummary):
    description: str
    constraints: str
    input_format: str
    output_format: str
    examples: List[dict]
    starter_code_python: str
    starter_code_java: str
    sample_test_cases: List[dict]
    highest_hint_level_used: int = 0

class CodeRunRequest(BaseModel):
    problem_id: Optional[int] = None
    language: str # python or java
    code: str
    custom_input: Optional[str] = None

class CodeSubmitRequest(BaseModel):
    problem_id: int
    language: str # python or java
    code: str

class TestCaseResult(BaseModel):
    test_case_id: int
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    error: Optional[str] = None
    runtime_ms: float = 0.0

class CodeRunResponse(BaseModel):
    status: str # "Success", "Wrong Answer", "Error", "Time Limit Exceeded"
    stdout: str
    stderr: str
    runtime_ms: float
    passed_tests: int
    total_tests: int
    test_results: List[TestCaseResult]
    ai_feedback: Optional[str] = None

class HintRequest(BaseModel):
    problem_id: int
    level: int # 1, 2, 3, 4, 5... unlimited progressive levels
    current_code: Optional[str] = None

class HintResponse(BaseModel):
    level: int
    title: str
    content: str
