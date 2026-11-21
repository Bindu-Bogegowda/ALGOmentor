from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import UserProblemStatus, HintUsage
from app.schemas.problem import HintRequest, HintResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/hints", tags=["Progressive Hints"])

@router.post("", response_model=HintResponse)
def get_progressive_hint(
    req: HintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prob = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")

    level = req.level
    if level not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Hint level must be 1, 2, or 3")

    # Record hint usage
    usage = HintUsage(
        user_id=current_user.id,
        problem_id=prob.id,
        hint_level=level
    )
    db.add(usage)

    # Update highest hint level in status
    status_rec = db.query(UserProblemStatus).filter(
        UserProblemStatus.user_id == current_user.id,
        UserProblemStatus.problem_id == prob.id
    ).first()
    if status_rec:
        status_rec.highest_hint_level_used = max(status_rec.highest_hint_level_used, level)
    else:
        status_rec = UserProblemStatus(
            user_id=current_user.id,
            problem_id=prob.id,
            highest_hint_level_used=level
        )
        db.add(status_rec)
    db.commit()

    if level == 1:
        return HintResponse(
            level=1,
            title="Level 1: Conceptual Clue",
            content=prob.hint_level_1
        )
    elif level == 2:
        return HintResponse(
            level=2,
            title="Level 2: Algorithmic Direction",
            content=prob.hint_level_2
        )
    else:
        return HintResponse(
            level=3,
            title="Level 3: Pseudocode Architecture",
            content=prob.hint_level_3
        )
