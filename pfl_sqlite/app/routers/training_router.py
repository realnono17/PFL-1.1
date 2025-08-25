from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.training_schema import TrainingSessionCreate, TrainingSessionUpdate, TrainingSessionOut
from app.models.training_session import TrainingSession
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/training", tags=["Training Sessions"])


@router.get("/", response_model=List[TrainingSessionOut])
def get_all_training_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return db.query(TrainingSession).all()


@router.get("/{session_id}", response_model=TrainingSessionOut)
def get_training_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if current_user.role != "admin" and current_user.club_id != session.club_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session")

    return session


@router.post("/", response_model=TrainingSessionOut)
def create_training_session(
    data: TrainingSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.club_id != data.club_id:
        raise HTTPException(status_code=403, detail="Not authorized to create for this club")

    session = TrainingSession(**data.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.put("/{session_id}", response_model=TrainingSessionOut)
def update_training_session(
    session_id: int,
    data: TrainingSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if current_user.role != "admin" and current_user.club_id != session.club_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}")
def delete_training_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(session)
    db.commit()
    return {"detail": "Training session deleted"}
