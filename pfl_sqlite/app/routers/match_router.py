from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.match import Match
from app.models.league_standing import LeagueStanding
from app.models.competition import Competition
from app.schemas.match_schema import MatchCreate, MatchUpdate, MatchOut
from app.database import get_db
from app.dependencies import require_admin

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/", response_model=List[MatchOut])
def get_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/", response_model=MatchOut)  # dependencies=[Depends(require_admin)])
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.put("/{match_id}", response_model=MatchOut)  # dependencies=[Depends(require_admin)])
def update_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = db.query(Match).get(match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Compare old vs new result
    result_before = (db_match.home_score, db_match.away_score)

    for key, value in match.model_dump().items():
        setattr(db_match, key, value)

    db.commit()
    db.refresh(db_match)

    result_after = (db_match.home_score, db_match.away_score)

    if result_before != result_after and None not in result_after:
        competition = db.query(Competition).get(db_match.competition_id)
        if competition and competition.name in ["PFL1", "PFL2"]:
            update_standings(db, db_match)

    return db_match


@router.delete("/{match_id}")  # dependencies=[Depends(require_admin)])
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).get(match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return {"detail": f"Match {match_id} deleted"}


def update_standings(db: Session, match: Match):
    season_id = match.season_id
    competition_id = match.competition_id

    def get_or_create_standing(club_id):
        standing = db.query(LeagueStanding).filter_by(
            season_id=season_id,
            competition_id=competition_id,
            club_id=club_id
        ).first()
        if not standing:
            standing = LeagueStanding(
                season_id=season_id,
                competition_id=competition_id,
                club_id=club_id,
                points=0,
                played=0,
                won=0,
                drawn=0,
                lost=0,
                goals_for=0,
                goals_against=0,
                goal_difference=0
            )
            db.add(standing)
            db.commit()
            db.refresh(standing)
        return standing

    home = get_or_create_standing(match.home_club_id)
    away = get_or_create_standing(match.away_club_id)

    home.played += 1
    away.played += 1

    home.goals_for += match.home_score
    home.goals_against += match.away_score

    away.goals_for += match.away_score
    away.goals_against += match.home_score

    if match.home_score > match.away_score:
        home.won += 1
        home.points += 3
        away.lost += 1
    elif match.away_score > match.home_score:
        away.won += 1
        away.points += 3
        home.lost += 1
    else:
        home.drawn += 1
        away.drawn += 1
        home.points += 1
        away.points += 1

    home.goal_difference = home.goals_for - home.goals_against
    away.goal_difference = away.goals_for - away.goals_against

    db.commit()
@router.get("/matches/upcoming", response_model=List[MatchOut])
def get_upcoming_matches(db: Session = Depends(get_db)):
    return (
        db.query(Match)
        .filter(Match.home_score == None)
        .order_by(Match.matchday_id.asc())
        .limit(10)
        .all()
    )
