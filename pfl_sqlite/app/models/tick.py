from sqlalchemy.orm import Session
from app.models.season import Season
from app.models.matchday import Matchday
from app.training.training_engine import trigger_training  # optional training hook

def perform_tick(db: Session):
    # Get the current season
    season = db.query(Season).filter(Season.is_current == True).first()
    if not season:
        raise ValueError("❌ No current season found.")

    if season.current_matchday > 18:
        raise ValueError("🏁 Season has already ended.")

    # Mark current matchday as completed
    matchday = (
        db.query(Matchday)
        .filter(Matchday.number == season.current_matchday, Matchday.season_id == season.id)
        .first()
    )
    if matchday:
        matchday.is_completed = True
        db.add(matchday)

    # Trigger training if MD9 or MD18
    if season.current_matchday in [9, 18]:
        print(f"🔥 Training triggered for matchday {season.current_matchday}")
        trigger_training(db, season.id)

    # Advance the tick
    season.current_matchday += 1
    db.add(season)
    db.commit()

    return {"message": f"✅ Matchday {season.current_matchday - 1} completed. Now on MD{season.current_matchday}."}
