from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.finance import Finance
from app.schemas.finance_schema import FinanceCreate, FinanceUpdate, FinanceOut
from app.database import get_db
from app.dependencies import require_admin, restrict_to_club

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/", response_model=List[FinanceOut], dependencies=[Depends(require_admin)])
def get_all_finances(db: Session = Depends(get_db)):
    return db.query(Finance).all()


@router.get("/{club_id}", response_model=FinanceOut)
def get_finance_by_club(club_id: int, allowed=Depends(lambda: restrict_to_club(club_id)), db: Session = Depends(get_db)):
    finance = db.query(Finance).filter(Finance.club_id == club_id).first()
    if not finance:
        raise HTTPException(status_code=404, detail="Finance not found for this club")
    return finance


@router.post("/", response_model=FinanceOut, dependencies=[Depends(require_admin)])
def create_finance(finance: FinanceCreate, db: Session = Depends(get_db)):
    db_finance = Finance(**finance.model_dump())
    db.add(db_finance)
    db.commit()
    db.refresh(db_finance)
    return db_finance


@router.put("/{club_id}", response_model=FinanceOut, dependencies=[Depends(require_admin)])
def update_finance(club_id: int, update: FinanceUpdate, db: Session = Depends(get_db)):
    finance = db.query(Finance).filter(Finance.club_id == club_id).first()
    if not finance:
        raise HTTPException(status_code=404, detail="Finance not found")
    for key, value in update.model_dump().items():
        setattr(finance, key, value)
    db.commit()
    db.refresh(finance)
    return finance


@router.delete("/{club_id}", dependencies=[Depends(require_admin)])
def delete_finance(club_id: int, db: Session = Depends(get_db)):
    finance = db.query(Finance).filter(Finance.club_id == club_id).first()
    if not finance:
        raise HTTPException(status_code=404, detail="Finance not found")
    db.delete(finance)
    db.commit()
    return {"detail": f"Finance for club {club_id} deleted"}
