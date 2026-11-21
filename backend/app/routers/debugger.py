from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.ai import DebugAnalyzeRequest, DebugAnalyzeResponse
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/debugger", tags=["Intelligent Code Debugger"])

@router.post("/analyze", response_model=DebugAnalyzeResponse)
def analyze_solution(
    req: DebugAnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = AIService.analyze_code_for_debugging(
        language=req.language,
        code=req.code,
        problem_description=req.problem_description,
        runtime_error=req.runtime_error,
        failed_test_case=req.failed_test_case
    )
    return DebugAnalyzeResponse(**analysis)
