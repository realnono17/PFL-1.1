from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.league_standing import LeagueStanding
from app.schemas.league_standing_schema import LeagueStandingOut
from sqlalchemy import asc

router = APIRouter(prefix="/standings", tags=["Standings"])

@router.get("/season/{season_id}/{competition_id}", response_model=List[LeagueStandingOut])
def get_standings(season_id: int, competition_id: int, db: Session = Depends(get_db)):
    return db.query(LeagueStanding).filter_by(
        season_id=season_id,
        competition_id=competition_id
    ).order_by(
        LeagueStanding.points.desc(),
        LeagueStanding.goal_difference.desc(),
        LeagueStanding.goals_for.desc()
    ).all()

@router.get("/season/{season_id}", response_model=List[LeagueStandingOut])
def get_all_standings_for_season(season_id: int, db: Session = Depends(get_db)):
    return db.query(LeagueStanding).filter(
        LeagueStanding.season_id == season_id
    ).order_by(
        LeagueStanding.competition_id.asc(),
        LeagueStanding.points.desc(),
        LeagueStanding.goal_difference.desc(),
        LeagueStanding.goals_for.desc()
    ).all()
@router.get("/league-standings/{competition_id}", response_model=List[LeagueStandingOut])
def get_standings_by_competition(competition_id: int, db: Session = Depends(get_db)):
    from app.models.season import Season

    # Get current season
    current_season = db.query(Season).filter(Season.is_current == True).first()
    if not current_season:
        raise HTTPException(status_code=404, detail="No current season found")

    # Return only standings for the current season + this competition
    standings = (
        db.query(LeagueStanding)
        .filter(
            LeagueStanding.competition_id == competition_id,
            LeagueStanding.season_id == current_season.id
        )
        .order_by(
            LeagueStanding.points.desc(),
            LeagueStanding.goal_difference.desc(),
            LeagueStanding.goals_for.desc()
        )
        .all()
    )
    return standings
