from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seed_data import seed_database
import app.models # ensure all models are registered

# Import routers
from app.routers import (
    auth, dashboard, roadmaps, lessons, problems,
    execution, hints, debugger, ai_tutor, projects,
    progress, streaks, analytics, reviews, profile
)

# Ensure database tables and initial curriculum are seeded
Base.metadata.create_all(bind=engine)
_db = SessionLocal()
try:
    seed_database(_db)
finally:
    _db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AlgoMentor - AI-powered algorithm learning and project development platform"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
prefix = settings.API_PREFIX
app.include_router(auth.router, prefix=prefix)
app.include_router(dashboard.router, prefix=prefix)
app.include_router(roadmaps.router, prefix=prefix)
app.include_router(lessons.router, prefix=prefix)
app.include_router(problems.router, prefix=prefix)
app.include_router(execution.router, prefix=prefix)
app.include_router(hints.router, prefix=prefix)
app.include_router(debugger.router, prefix=prefix)
app.include_router(ai_tutor.router, prefix=prefix)
app.include_router(projects.router, prefix=prefix)
app.include_router(progress.router, prefix=prefix)
app.include_router(streaks.router, prefix=prefix)
app.include_router(analytics.router, prefix=prefix)
app.include_router(reviews.router, prefix=prefix)
app.include_router(profile.router, prefix=prefix)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "tagline": "Learn Algorithms. Master Logic. Build Anything.",
        "version": settings.VERSION,
        "api_docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
