from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ai-tutor", tags=["AI Personal Tutor"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find or create session
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == req.session_id,
            ChatSession.user_id == current_user.id
        ).first()

    if not session:
        session = ChatSession(
            user_id=current_user.id,
            title=f"Chat: {req.problem_title or req.context_page or 'Algorithm Inquiry'}",
            context_page=req.context_page or "general"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=req.message,
        code_snippet=req.current_code
    )
    db.add(user_msg)
    db.commit()

    # Generate AI response
    ai_result = await AIService.chat_tutor(
        message=req.message,
        context_page=req.context_page or "general",
        current_code=req.current_code,
        problem_title=req.problem_title,
        error_message=req.error_message,
        student_level=current_user.difficulty_level or "Beginner"
    )

    # Save assistant message
    asst_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=ai_result["reply"],
        code_snippet=ai_result.get("code_suggestion")
    )
    db.add(asst_msg)
    db.commit()

    return ChatResponse(
        session_id=session.id,
        reply=ai_result["reply"],
        code_suggestion=ai_result.get("code_suggestion")
    )

@router.get("/history/{session_id}")
def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        return {"messages": []}

    msgs = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.created_at).all()
    return {
        "session_id": session.id,
        "title": session.title,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "code_snippet": m.code_snippet,
                "created_at": m.created_at.strftime("%H:%M")
            }
            for m in msgs
        ]
    }
