from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import UserProblemStatus
from app.schemas.problem import ProblemSummary, ProblemDetail
from app.services.auth_service import get_current_user
from app.routers.hints import _generate_edge_cases_hint, _generate_code_skeleton_hint, _generate_complexity_hint

router = APIRouter(prefix="/problems", tags=["Practice Problem Bank"])

@router.get("", response_model=List[ProblemSummary])
def list_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    pattern: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Problem)
    if topic:
        query = query.filter(Problem.topic.ilike(f"%{topic}%"))
    if difficulty:
        query = query.filter(Problem.difficulty.ilike(difficulty))
    if pattern:
        query = query.filter(Problem.algorithmic_pattern.ilike(f"%{pattern}%"))
    if search:
        query = query.filter(Problem.title.ilike(f"%{search}%"))

    problems = query.all()
    results = []

    for p in problems:
        status_rec = db.query(UserProblemStatus).filter(
            UserProblemStatus.user_id == current_user.id,
            UserProblemStatus.problem_id == p.id
        ).first()

        results.append(ProblemSummary(
            id=p.id,
            slug=p.slug,
            title=p.title,
            topic=p.topic,
            subtopic=p.subtopic,
            algorithmic_pattern=p.algorithmic_pattern,
            difficulty=p.difficulty,
            expected_time_complexity=p.expected_time_complexity,
            expected_space_complexity=p.expected_space_complexity,
            status=status_rec.status if status_rec else "Unsolved",
            is_bookmarked=status_rec.is_bookmarked if status_rec else False,
            is_in_revision=status_rec.is_in_revision if status_rec else False
        ))

    return results

@router.get("/{slug}", response_model=ProblemDetail)
def get_problem(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    p = db.query(Problem).filter(Problem.slug == slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    status_rec = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.problem_id == p.id
    ).first()

    problem_hints = [
        {"level": 1, "title": "Level 1: Conceptual Clue", "content": p.hint_level_1},
        {"level": 2, "title": "Level 2: Algorithmic Direction", "content": p.hint_level_2},
        {"level": 3, "title": "Level 3: Pseudocode Architecture", "content": p.hint_level_3},
        {"level": 4, "title": "Level 4: Edge Cases & Boundary Conditions", "content": _generate_edge_cases_hint(p)},
        {"level": 5, "title": "Level 5: Code Skeleton & Method Signatures", "content": _generate_code_skeleton_hint(p)},
        {"level": 6, "title": "Level 6: Complexity Bottleneck & Optimization", "content": _generate_complexity_hint(p)}
    ]

    return ProblemDetail(
        id=p.id,
        slug=p.slug,
        title=p.title,
        topic=p.topic,
        subtopic=p.subtopic,
        algorithmic_pattern=p.algorithmic_pattern,
        difficulty=p.difficulty,
        expected_time_complexity=p.expected_time_complexity,
        expected_space_complexity=p.expected_space_complexity,
        status=status_rec.status if status_rec else "Unsolved",
        is_bookmarked=status_rec.is_bookmarked if status_rec else False,
        is_in_revision=status_rec.is_in_revision if status_rec else False,
        description=p.description,
        constraints=p.constraints,
        input_format=p.input_format,
        output_format=p.output_format,
        examples=json.loads(p.examples_json),
        starter_code_python=p.starter_code_python,
        starter_code_java=p.starter_code_java,
        sample_test_cases=json.loads(p.sample_test_cases),
        highest_hint_level_used=status_rec.highest_hint_level_used if status_rec else 0,
        hints=problem_hints
    )

@router.post("/{slug}/bookmark")
def toggle_bookmark(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    p = db.query(Problem).filter(Problem.slug == slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    status_rec = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.problem_id == p.id
    ).first()

    if not status_rec:
        status_rec = UserProblemStatus(
            user_id=current_user.id,
            problem_id=p.id,
            is_bookmarked=True
        )
        db.add(status_rec)
    else:
        status_rec.is_bookmarked = not status_rec.is_bookmarked

    db.commit()
    return {"is_bookmarked": status_rec.is_bookmarked}
