import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.lesson import Lesson, UserLessonProgress
from app.models.activity import ActivityLog
from app.services.activity_service import record_user_activity
from app.schemas.lesson import (
    LessonSummary,
    LessonDetail,
    LessonProgressUpdate,
    LessonQuizSubmit,
    LessonQuizResult,
    DependencyGraphNode,
    DependencyGraphEdge,
    DependencyGraphResponse
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/lessons", tags=["Concept Lessons"])

@router.get("", response_model=List[LessonSummary])
def list_lessons(
    topic_id: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)
    if topic_id:
        query = query.filter(Lesson.topic_id == topic_id)
    if category and category.lower() != "all":
        query = query.filter(Lesson.category.ilike(f"%{category}%"))
    if difficulty and difficulty.lower() != "all":
        query = query.filter(Lesson.difficulty.ilike(f"%{difficulty}%"))
    if search:
        s_term = f"%{search}%"
        query = query.filter((Lesson.title.ilike(s_term)) | (Lesson.summary.ilike(s_term)))
    lessons = query.order_by(Lesson.level_number.asc().nullslast(), Lesson.step_number.asc().nullslast(), Lesson.order_index.asc().nullslast(), Lesson.title.asc()).all()

    results = []
    for l in lessons:
        prog = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.lesson_id == l.id
        ).first()
        results.append(LessonSummary(
            id=l.id,
            topic_id=l.topic_id,
            category=l.category or "DSA",
            difficulty=l.difficulty or "Beginner",
            prerequisites=l.prerequisites or "None",
            title=l.title,
            summary=l.summary,
            time_complexity=l.time_complexity or "O(n)",
            space_complexity=l.space_complexity or "O(1)",
            visualization_type=l.visualization_type,
            visualization_algorithm=l.visualization_algorithm,
            is_completed=prog.is_completed if prog else False,
            mastery_level=prog.mastery_level if prog else "not_started",
            quiz_score=prog.quiz_score if prog else 0,
            order_index=l.order_index or 0,
            step_number=l.step_number or 1,
            stage_name=l.stage_name or "Core Foundations",
            level_number=l.level_number or 1,
            level_title=l.level_title or "Level 1: Programming Foundations",
            prev_lesson_id=l.prev_lesson_id,
            next_lesson_id=l.next_lesson_id
        ))
    return results

@router.get("/dependency-graph", response_model=DependencyGraphResponse)
def get_dependency_graph(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns all curriculum concept nodes and their prerequisite edges for interactive visualization."""
    lessons = db.query(Lesson).order_by(Lesson.step_number).all()
    
    nodes = []
    edges = []
    lesson_map = {l.id: l for l in lessons}
    
    for l in lessons:
        prog = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.lesson_id == l.id
        ).first()
        
        nodes.append(DependencyGraphNode(
            id=l.id,
            title=l.title,
            level_number=l.level_number or 1,
            level_title=l.level_title or "Foundations",
            category=l.category or "dsa",
            difficulty=l.difficulty or "Beginner",
            is_completed=prog.is_completed if prog else False,
            mastery_level=prog.mastery_level if prog else "not_started",
            step_number=l.step_number or 1
        ))
        
        # Sequential edge
        if l.next_lesson_id and l.next_lesson_id in lesson_map:
            edges.append(DependencyGraphEdge(
                source=l.id,
                target=l.next_lesson_id,
                type="next_step"
            ))
            
        # Prerequisite edge from concept_connections
        if l.concept_connections:
            try:
                conns = json.loads(l.concept_connections)
                prereqs = conns.get("prerequisites", [])
                for p in prereqs:
                    if p in lesson_map:
                        edges.append(DependencyGraphEdge(
                            source=p,
                            target=l.id,
                            type="prerequisite"
                        ))
            except Exception:
                pass
                
    return DependencyGraphResponse(nodes=nodes, edges=edges)

@router.get("/{lesson_id}", response_model=LessonDetail)
def get_lesson(
    lesson_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    prog = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.lesson_id == lesson.id
    ).first()

    prev_title = None
    next_title = None
    if lesson.prev_lesson_id:
        prev_l = db.query(Lesson).filter(Lesson.id == lesson.prev_lesson_id).first()
        if prev_l:
            prev_title = prev_l.title
    if lesson.next_lesson_id:
        next_l = db.query(Lesson).filter(Lesson.id == lesson.next_lesson_id).first()
        if next_l:
            next_title = next_l.title

    return LessonDetail(
        id=lesson.id,
        topic_id=lesson.topic_id,
        category=lesson.category or "dsa",
        difficulty=lesson.difficulty or "Beginner",
        title=lesson.title,
        summary=lesson.summary,
        fundamental_explanation=lesson.fundamental_explanation,
        step_by_step=lesson.step_by_step,
        real_world_applications=lesson.real_world_applications or lesson.why_learn_it or "",
        examples_illustrations=lesson.examples_illustrations,
        pseudocode=lesson.pseudocode,
        time_complexity=lesson.time_complexity or "O(n)",
        space_complexity=lesson.space_complexity or "O(1)",
        prerequisites=lesson.prerequisites or "Programming Basics",
        related_concepts=lesson.related_concepts or "",
        video_url=lesson.video_url,
        video_title=lesson.video_title,
        visualization_type=lesson.visualization_type,
        visualization_algorithm=lesson.visualization_algorithm,
        practice_problem_slug=lesson.practice_problem_slug,
        is_completed=prog.is_completed if prog else False,
        mastery_level=prog.mastery_level if prog else "not_started",
        quiz_score=prog.quiz_score if prog else 0,
        order_index=lesson.order_index or 0,
        step_number=lesson.step_number or 1,
        stage_name=lesson.stage_name or "Core Foundations",
        level_number=lesson.level_number or 1,
        level_title=lesson.level_title or "Level 1: Programming Foundations",
        prev_lesson_id=lesson.prev_lesson_id,
        next_lesson_id=lesson.next_lesson_id,
        prev_lesson_title=prev_title,
        next_lesson_title=next_title,
        why_learn_it=lesson.why_learn_it or "",
        core_theory=lesson.core_theory or lesson.step_by_step or "",
        dry_run=lesson.dry_run or "[]",
        java_code=lesson.java_code or "",
        python_code=lesson.python_code or "",
        practice_questions=lesson.practice_questions or "[]",
        ai_hints=lesson.ai_hints or "[]",
        common_mistakes=lesson.common_mistakes or "",
        concept_connections=lesson.concept_connections or "{}",
        quiz_questions=lesson.quiz_questions or "[]",
        mastery_threshold=lesson.mastery_threshold or 70
    )

@router.post("/{lesson_id}/progress")
def update_lesson_progress(
    lesson_id: str,
    body: LessonProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    prog = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()

    if not prog:
        prog = UserLessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_completed=body.is_completed,
            completed_at=datetime.utcnow() if body.is_completed else None,
            time_spent_seconds=body.time_spent_seconds,
            mastery_level="proficient" if body.is_completed else "learning"
        )
        db.add(prog)
    else:
        prog.is_completed = body.is_completed
        if body.is_completed and not prog.completed_at:
            prog.completed_at = datetime.utcnow()
            if prog.mastery_level in ["not_started", "learning"]:
                prog.mastery_level = "proficient"
        prog.time_spent_seconds += body.time_spent_seconds

    if body.is_completed:
        record_user_activity(
            db=db,
            user_id=current_user.id,
            action_type="lesson_completed",
            topic=lesson.title,
            metadata_json={"lesson_id": lesson.id},
            active_seconds=body.time_spent_seconds
        )
    else:
        db.commit()
    return {"status": "success", "is_completed": prog.is_completed, "mastery_level": prog.mastery_level}

@router.post("/{lesson_id}/quiz", response_model=LessonQuizResult)
def submit_lesson_quiz(
    lesson_id: str,
    body: LessonQuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Evaluates student quiz submission, calculates score, updates mastery status and unlocks next lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    questions = []
    if lesson.quiz_questions:
        try:
            questions = json.loads(lesson.quiz_questions)
        except Exception:
            questions = []

    if not questions:
        raise HTTPException(status_code=400, detail="No quiz available for this concept")

    correct_count = 0
    total = len(questions)

    for i, q in enumerate(questions):
        q_key = str(i)
        # Check if student answered
        chosen = body.answers.get(q_key)
        if chosen is None:
            chosen = body.answers.get(str(q.get("id", i + 1)))
        if chosen is not None and int(chosen) == int(q.get("correct_idx", 0)):
            correct_count += 1

    score_percent = int((correct_count / total) * 100) if total > 0 else 0
    threshold = lesson.mastery_threshold or 70
    is_passed = score_percent >= threshold

    mastery_level = "learning"
    if score_percent >= 90:
        mastery_level = "mastered"
    elif score_percent >= threshold:
        mastery_level = "proficient"

    prog = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()

    if not prog:
        prog = UserLessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_completed=is_passed,
            completed_at=datetime.utcnow() if is_passed else None,
            time_spent_seconds=180,
            quiz_score=score_percent,
            mastery_level=mastery_level
        )
        db.add(prog)
    else:
        if score_percent > (prog.quiz_score or 0):
            prog.quiz_score = score_percent
        if is_passed:
            prog.is_completed = True
            if not prog.completed_at:
                prog.completed_at = datetime.utcnow()
            prog.mastery_level = mastery_level

    # Log quiz activity with streak synchronization
    record_user_activity(
        db=db,
        user_id=current_user.id,
        action_type="quiz_completed",
        topic=f"Quiz: {lesson.title}",
        metadata_json={"lesson_id": lesson.id, "score": score_percent, "is_passed": is_passed},
        active_seconds=120
    )

    feedback = (
        f"Outstanding! You scored {score_percent}% and mastered {lesson.title}."
        if is_passed
        else f"You scored {score_percent}% (passing threshold is {threshold}%). Review the theory and try again to unlock the next level!"
    )

    return LessonQuizResult(
        score_percent=score_percent,
        correct_count=correct_count,
        total_questions=total,
        is_passed=is_passed,
        mastery_level=mastery_level,
        feedback=feedback,
        unlocked_next_lesson_id=lesson.next_lesson_id if is_passed else None
    )
