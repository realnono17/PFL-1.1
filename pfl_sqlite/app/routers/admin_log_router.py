from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.admin_log import AdminLog
from app.schemas.admin_log_schema import AdminLogCreate, AdminLogOut
from app.database import get_db
from app.dependencies import require_admin

router = APIRouter(prefix="/admin-logs", tags=["Admin Logs"])


@router.get("/", response_model=List[AdminLogOut], dependencies=[Depends(require_admin)])
def get_logs(db: Session = Depends(get_db)):
    return db.query(AdminLog).order_by(AdminLog.timestamp.desc()).all()


@router.post("/", response_model=AdminLogOut, dependencies=[Depends(require_admin)])
def create_log(log: AdminLogCreate, db: Session = Depends(get_db)):
    new_log = AdminLog(**log.model_fields)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


@router.get("/{log_id}", response_model=AdminLogOut, dependencies=[Depends(require_admin)])
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AdminLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
