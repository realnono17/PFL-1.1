from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.tactic import Tactic
from app.schemas.tactic_schema import TacticCreate, TacticUpdate, TacticOut
from app.database import get_db
from app.dependencies import require_admin

router = APIRouter(prefix="/tactics", tags=["Tactics"])


@router.get("/", response_model=List[TacticOut])
def get_tactics(db: Session = Depends(get_db)):
    return db.query(Tactic).all()


@router.get("/{tactic_id}", response_model=TacticOut)
def get_tactic(tactic_id: int, db: Session = Depends(get_db)):
    tactic = db.query(Tactic).get(tactic_id)
    if not tactic:
        raise HTTPException(status_code=404, detail="Tactic not found")
    return tactic


@router.post("/", response_model=TacticOut, dependencies=[Depends(require_admin)])
def create_tactic(tactic: TacticCreate, db: Session = Depends(get_db)):
    db_tactic = Tactic(**tactic.model_dump())
    db.add(db_tactic)
    db.commit()
    db.refresh(db_tactic)
    return db_tactic


@router.put("/{tactic_id}", response_model=TacticOut, dependencies=[Depends(require_admin)])
def update_tactic(tactic_id: int, tactic: TacticUpdate, db: Session = Depends(get_db)):
    db_tactic = db.query(Tactic).get(tactic_id)
    if not db_tactic:
        raise HTTPException(status_code=404, detail="Tactic not found")
    for key, value in tactic.model_dump().items():
        setattr(db_tactic, key, value)
    db.commit()
    db.refresh(db_tactic)
    return db_tactic


@router.delete("/{tactic_id}", dependencies=[Depends(require_admin)])
def delete_tactic(tactic_id: int, db: Session = Depends(get_db)):
    db_tactic = db.query(Tactic).get(tactic_id)
    if not db_tactic:
        raise HTTPException(status_code=404, detail="Tactic not found")
    db.delete(db_tactic)
    db.commit()
    return {"detail": f"Tactic {tactic_id} deleted"}
