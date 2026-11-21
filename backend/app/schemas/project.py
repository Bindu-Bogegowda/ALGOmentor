from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectFileSchema(BaseModel):
    id: Optional[int] = None
    filename: str
    filepath: Optional[str] = ""
    content: str
    language: str

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    project_type: str = "web_interactive" # web_interactive, algorithm_benchmark, python_script
    prompt_idea: Optional[str] = ""
    tags: Optional[str] = "algorithms,frontend"
    files: List[ProjectFileSchema] = []

class ProjectGenerateRequest(BaseModel):
    prompt: str
    project_type: str = "web_interactive" # web_interactive, algorithm_benchmark, python_script
    target_framework: Optional[str] = "html_js"

class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    project_type: str
    prompt_idea: str
    tags: str
    files: List[ProjectFileSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
