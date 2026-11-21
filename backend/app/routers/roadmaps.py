from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.roadmap import RoadmapStream, RoadmapTopic, UserTopicProgress
from app.schemas.roadmap import RoadmapStreamDetail, RoadmapTopicItem
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])

@router.get("", response_model=List[RoadmapStreamDetail])
def list_roadmap_streams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    streams = db.query(RoadmapStream).order_index = db.query(RoadmapStream).order_by(RoadmapStream.order_index).all()
    results = []

    for s in streams:
        topics = db.query(RoadmapTopic).filter(RoadmapTopic.stream_id == s.id).order_by(RoadmapTopic.order_index).all()
        topic_items = []
        completed_count = 0

        for t in topics:
            user_prog = db.query(UserTopicProgress).filter(
                UserTopicProgress.user_id == current_user.id,
                UserTopicProgress.topic_id == t.id
            ).first()

            is_comp = user_prog.is_completed if user_prog else False
            if is_comp:
                completed_count += 1

            topic_items.append(RoadmapTopicItem(
                id=t.id,
                stream_id=t.stream_id,
                title=t.title,
                level=t.level,
                description=t.description,
                estimated_minutes=t.estimated_minutes,
                order_index=t.order_index,
                prerequisite_topic_id=t.prerequisite_topic_id,
                milestone_tag=t.milestone_tag,
                is_unlocked=user_prog.is_unlocked if user_prog else True,
                is_completed=is_comp,
                progress_percentage=user_prog.progress_percentage if user_prog else 0.0
            ))

        pct = round((completed_count / max(1, len(topics))) * 100, 1)

        results.append(RoadmapStreamDetail(
            id=s.id,
            title=s.title,
            description=s.description,
            category=s.category,
            icon=s.icon,
            total_hours_estimate=s.total_hours_estimate,
            prerequisites=s.prerequisites,
            topics=topic_items,
            user_completion_pct=pct
        ))

    return results

@router.get("/{stream_id}", response_model=RoadmapStreamDetail)
def get_roadmap_stream(
    stream_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    s = db.query(RoadmapStream).filter(RoadmapStream.id == stream_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Roadmap stream not found")

    topics = db.query(RoadmapTopic).filter(RoadmapTopic.stream_id == s.id).order_by(RoadmapTopic.order_index).all()
    topic_items = []
    completed_count = 0

    for t in topics:
        user_prog = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == current_user.id,
            UserTopicProgress.topic_id == t.id
        ).first()

        is_comp = user_prog.is_completed if user_prog else False
        if is_comp:
            completed_count += 1

        topic_items.append(RoadmapTopicItem(
            id=t.id,
            stream_id=t.stream_id,
            title=t.title,
            level=t.level,
            description=t.description,
            estimated_minutes=t.estimated_minutes,
            order_index=t.order_index,
            prerequisite_topic_id=t.prerequisite_topic_id,
            milestone_tag=t.milestone_tag,
            is_unlocked=user_prog.is_unlocked if user_prog else True,
            is_completed=is_comp,
            progress_percentage=user_prog.progress_percentage if user_prog else 0.0
        ))

    pct = round((completed_count / max(1, len(topics))) * 100, 1)

    return RoadmapStreamDetail(
        id=s.id,
        title=s.title,
        description=s.description,
        category=s.category,
        icon=s.icon,
        total_hours_estimate=s.total_hours_estimate,
        prerequisites=s.prerequisites,
        topics=topic_items,
        user_completion_pct=pct
    )
