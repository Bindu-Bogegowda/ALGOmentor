from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    context_page: Optional[str] = "general"
    message: str
    current_code: Optional[str] = None
    problem_title: Optional[str] = None
    error_message: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: int
    reply: str
    code_suggestion: Optional[str] = None

class DebugAnalyzeRequest(BaseModel):
    language: str
    code: str
    problem_description: Optional[str] = None
    runtime_error: Optional[str] = None
    failed_test_case: Optional[Dict[str, Any]] = None

class DebugAnalyzeResponse(BaseModel):
    error_type: str # Syntax, Runtime, Logical, TimeComplexity, SpaceComplexity, EdgeCase
    summary: str
    why_it_happened: str
    how_to_fix: str
    suggested_approach: str
    pseudocode_hint: Optional[str] = None
