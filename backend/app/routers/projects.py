from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.project import Project, ProjectFile
from app.models.activity import ActivityLog
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectGenerateRequest, ProjectFileSchema
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/projects", tags=["AI Project Builder"])

@router.get("", response_model=List[ProjectResponse])
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.updated_at.desc()).all()
    results = []
    for p in projects:
        files = db.query(ProjectFile).filter(ProjectFile.project_id == p.id).all()
        results.append(ProjectResponse(
            id=p.id,
            user_id=p.user_id,
            title=p.title,
            description=p.description or "",
            project_type=p.project_type,
            prompt_idea=p.prompt_idea or "",
            tags=p.tags or "",
            files=[
                ProjectFileSchema(
                    id=f.id,
                    filename=f.filename,
                    filepath=f.filepath or "",
                    content=f.content,
                    language=f.language
                )
                for f in files
            ],
            created_at=p.created_at,
            updated_at=p.updated_at
        ))
    return results

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    p = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    files = db.query(ProjectFile).filter(ProjectFile.project_id == p.id).all()
    return ProjectResponse(
        id=p.id,
        user_id=p.user_id,
        title=p.title,
        description=p.description or "",
        project_type=p.project_type,
        prompt_idea=p.prompt_idea or "",
        tags=p.tags or "",
        files=[
            ProjectFileSchema(
                id=f.id,
                filename=f.filename,
                filepath=f.filepath or "",
                content=f.content,
                language=f.language
            )
            for f in files
        ],
        created_at=p.created_at,
        updated_at=p.updated_at
    )

@router.post("/generate", response_model=ProjectResponse)
def generate_project_with_ai(
    req: ProjectGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gen_data = AIService.generate_project(req.prompt, req.project_type)

    new_project = Project(
        user_id=current_user.id,
        title=gen_data["title"],
        description=gen_data["description"],
        project_type=gen_data["project_type"],
        prompt_idea=req.prompt,
        tags=gen_data.get("tags", "algorithms,interactive")
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    created_files = []
    for f_info in gen_data["files"]:
        pf = ProjectFile(
            project_id=new_project.id,
            filename=f_info["filename"],
            filepath=f_info.get("filepath", f_info["filename"]),
            content=f_info["content"],
            language=f_info.get("language", "javascript")
        )
        db.add(pf)
        db.commit()
        db.refresh(pf)
        created_files.append(pf)

    # Log activity
    act = ActivityLog(
        user_id=current_user.id,
        action_type="project_generated",
        topic=new_project.title,
        active_seconds=600
    )
    db.add(act)
    db.commit()

    return ProjectResponse(
        id=new_project.id,
        user_id=new_project.user_id,
        title=new_project.title,
        description=new_project.description or "",
        project_type=new_project.project_type,
        prompt_idea=new_project.prompt_idea or "",
        tags=new_project.tags or "",
        files=[
            ProjectFileSchema(
                id=f.id,
                filename=f.filename,
                filepath=f.filepath or "",
                content=f.content,
                language=f.language
            )
            for f in created_files
        ],
        created_at=new_project.created_at,
        updated_at=new_project.updated_at
    )

@router.put("/{project_id}/files/{filename}")
def update_project_file(
    project_id: int,
    filename: str,
    file_data: ProjectFileSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    p = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    pf = db.query(ProjectFile).filter(ProjectFile.project_id == p.id, ProjectFile.filename == filename).first()
    if not pf:
        pf = ProjectFile(
            project_id=p.id,
            filename=filename,
            filepath=file_data.filepath or filename,
            content=file_data.content,
            language=file_data.language
        )
        db.add(pf)
    else:
        pf.content = file_data.content
        pf.language = file_data.language
        pf.updated_at = datetime.utcnow()

    p.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "saved", "filename": filename}
