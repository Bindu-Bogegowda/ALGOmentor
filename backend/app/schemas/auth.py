from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = "Algorithm Explorer"
    preferred_language: Optional[str] = "python"
    difficulty_level: Optional[str] = "Beginner"

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    reset_token: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    avatar: str
    bio: str
    preferred_language: str
    difficulty_level: str
    active_roadmap: str
    theme: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    preferred_language: Optional[str] = None
    difficulty_level: Optional[str] = None
    active_roadmap: Optional[str] = None
    theme: Optional[str] = None
