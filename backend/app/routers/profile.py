from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse, UserUpdate
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/profile", tags=["Student Profile & Settings"])

@router.get("", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("", response_model=UserResponse)
def update_user_profile(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if body.full_name is not None:
        current_user.full_name = body.full_name
    if body.avatar is not None:
        current_user.avatar = body.avatar
    if body.bio is not None:
        current_user.bio = body.bio
    if body.preferred_language is not None:
        current_user.preferred_language = body.preferred_language
    if body.difficulty_level is not None:
        current_user.difficulty_level = body.difficulty_level
    if body.active_roadmap is not None:
        current_user.active_roadmap = body.active_roadmap
    if body.theme is not None:
        current_user.theme = body.theme

    db.commit()
    db.refresh(current_user)
    return current_user
