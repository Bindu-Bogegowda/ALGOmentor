import os
from pathlib import Path
from pydantic import BaseModel

BACKEND_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BACKEND_DIR / "algomentor.db"

class Settings(BaseModel):
    PROJECT_NAME: str = "AlgoMentor"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database - Always point directly to backend/algomentor.db
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "algomentor-super-secret-jwt-key-change-in-production-2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # AI API keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
    
    # Execution
    EXECUTION_ENGINE: str = os.getenv("EXECUTION_ENGINE", "isolated_local")
    PISTON_API_URL: str = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston")

settings = Settings()
