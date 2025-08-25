from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.season import Season
from app.models.matchday import Matchday
from app.schemas.tick_schema import TickResult
from datetime import datetime

router = APIRouter(prefix="/tick", tags=["League Tick"])

@router.post("/advance", response_model=TickResult)
def advance_tick(db: Session = Depends(get_db)):
    # Fetch current season
    current_season = db.query(Season).order_by(Season.id.desc()).first()
    if not current_season:
        raise HTTPException(status_code=404, detail="No active season found")

    # Fetch current matchday
    current_md = (
        db.query(Matchday)
        .filter(Matchday.season_id == current_season.id)
        .filter(Matchday.is_completed == False)
        .order_by(Matchday.number.asc())
        .first()
    )

    if not current_md:
        raise HTTPException(status_code=400, detail="All matchdays completed!")

    # Mark current matchday as completed
    current_md.is_completed = True
    db.commit()

    result_msg = f"Matchday {current_md.number} completed."

    # Mid-season training trigger
    if current_md.number == 9:
        result_msg += " Mid-season training triggered."
        # 🧠 Mid-season training logic here
        # trigger_training_regimes()

    # End-of-season logic
    if current_md.number == 18:
        result_msg += " End of season logic triggered."
        # 🧠 End-of-season logic here
        # trigger_final_training(), awards, contracts, etc.

    return TickResult(
        season_id=current_season.id,
        matchday_completed=current_md.number,
        message=result_msg
    )
