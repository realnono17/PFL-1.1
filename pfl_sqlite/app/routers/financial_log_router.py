# app/routers/financial_log_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.financial_log import FinancialLog
from app.schemas.financial_log_schema import FinancialLogCreate, FinancialLogOut

router = APIRouter(prefix="/logs", tags=["Financial Logs"])

@router.post("/", response_model=FinancialLogOut)
def create_log(log: FinancialLogCreate, db: Session = Depends(get_db)):
    db_log = FinancialLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/club/{club_id}", response_model=list[FinancialLogOut])
def get_logs_for_club(club_id: int, db: Session = Depends(get_db)):
    return db.query(FinancialLog).filter(FinancialLog.club_id == club_id).order_by(FinancialLog.timestamp.desc()).all()

@router.delete("/{log_id}", response_model=FinancialLogOut)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(FinancialLog).filter(FinancialLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Financial log not found")
    db.delete(log)
    db.commit()
    return log
