from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.match import Match
from app.schemas.match_schema import MatchOut

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/", response_model=List[MatchOut])
def get_all_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()

@router.get("/season/{season_id}", response_model=List[MatchOut])
def get_matches_by_season(season_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.season_id == season_id).all()

@router.get("/matchday/{matchday_id}", response_model=List[MatchOut])
def get_matches_by_matchday(matchday_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.matchday_id == matchday_id).all()

@router.get("/season/{season_id}/competition/{competition_id}", response_model=List[MatchOut])
def get_matches_by_season_and_comp(season_id: int, competition_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(
        Match.season_id == season_id,
        Match.competition_id == competition_id
    ).all()

@router.get("/matchday/{matchday_id}/competition/{competition_id}", response_model=List[MatchOut])
def get_matches_by_matchday_and_competition(
    matchday_id: int,
    competition_id: int,
    db: Session = Depends(get_db)
):
    matches = (
        db.query(Match)
        .filter(Match.matchday_id == matchday_id)
        .filter(Match.competition_id == competition_id)
        .all()
    )
    return matches

