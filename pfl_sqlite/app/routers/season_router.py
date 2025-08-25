from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.season import Season
from app.models.matchday import Matchday
from app.models.match import Match
from app.models.club import Club
from app.models.competition import Competition
from app.models.league_standing import LeagueStanding  # ✅ NEW
from app.schemas.season_schema import SeasonCreate, SeasonResponse
from datetime import datetime
import random

router = APIRouter(
    prefix="/seasons",
    tags=["Seasons"]
)

@router.post("/", response_model=SeasonResponse)
def create_season(season_data: SeasonCreate, db: Session = Depends(get_db)):
    # Step 1: Create Season
    new_season = Season(
        name=season_data.name,
        start_year=season_data.start_year,
        is_current=True,
        current_matchday=1
    )
    db.add(new_season)
    db.commit()
    db.refresh(new_season)

    # Step 2: Create Competitions
    pfl1_comp = Competition(name="PFL1", type="League", season_id=new_season.id)
    pfl2_comp = Competition(name="PFL2", type="League", season_id=new_season.id)
    copa_comp = Competition(name="Copa Barbanegra", type="Cup", season_id=new_season.id)

    db.add_all([pfl1_comp, pfl2_comp, copa_comp])
    db.commit()
    db.refresh(pfl1_comp)
    db.refresh(pfl2_comp)
    db.refresh(copa_comp)

    # Step 3: Fetch Clubs
    pfl1_clubs = db.query(Club).filter(Club.league == "PFL1", Club.is_controlled_by_player == True).all()
    pfl2_clubs = db.query(Club).filter(Club.league == "PFL2", Club.is_controlled_by_player == True).all()
    all_player_clubs = pfl1_clubs + pfl2_clubs

    random.shuffle(pfl1_clubs)
    random.shuffle(pfl2_clubs)

    # ✅ Step 4: Create LeagueStanding entries
    for club in pfl1_clubs:
        db.add(LeagueStanding(club_id=club.id, season_id=new_season.id, competition_id=pfl1_comp.id))
    for club in pfl2_clubs:
        db.add(LeagueStanding(club_id=club.id, season_id=new_season.id, competition_id=pfl2_comp.id))
    db.commit()

    # Step 5: Create Matchdays
    matchdays = []
    for i in range(1, 19):
        md = Matchday(number=i, season_id=new_season.id, is_completed=False)
        db.add(md)
        db.commit()
        matchdays.append(md)

    # Step 6: League Matches
    def create_league_matches(clubs, competition_id):
        schedule = generate_round_robin_schedule([club.id for club in clubs])
        for i, fixtures in enumerate(schedule):
            md = matchdays[i]
            for home_id, away_id in fixtures:
                match = Match(
                    home_club_id=home_id,
                    away_club_id=away_id,
                    matchday_id=md.id,
                    season_id=new_season.id,
                    competition_id=competition_id
                )
                db.add(match)

    create_league_matches(pfl1_clubs, pfl1_comp.id)
    create_league_matches(pfl2_clubs, pfl2_comp.id)

    # Step 7: Copa Barbanegra Knockouts
    copa_clubs = all_player_clubs
    random.shuffle(copa_clubs)
    if len(copa_clubs) < 16:
        raise HTTPException(status_code=400, detail="Not enough clubs for Copa Barbanegra")

    prelim = copa_clubs[:8]
    rest = copa_clubs[8:]

    md_offset = 2  # Matchday 3 (0-indexed)
    def add_cup_round(round_teams, label):
        nonlocal md_offset
        fixtures = list(zip(round_teams[::2], round_teams[1::2]))
        md = matchdays[md_offset]
        for home, away in fixtures:
            match = Match(
                home_club_id=home.id,
                away_club_id=away.id,
                matchday_id=md.id,
                season_id=new_season.id,
                competition_id=copa_comp.id
            )
            db.add(match)
        md_offset += 3
        return [home for home, away in fixtures]

    r16_teams = rest + add_cup_round(prelim, "Preliminary")
    r8 = add_cup_round(r16_teams, "R16")
    r4 = add_cup_round(r8, "Quarterfinal")
    r2 = add_cup_round(r4, "Semifinal")
    _ = add_cup_round(r2, "Final")

    db.commit()
    return new_season

@router.get("/", response_model=list[SeasonResponse])
def get_seasons(db: Session = Depends(get_db)):
    return db.query(Season).all()

@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    # Delete all matches from matchdays in this season
    for md in season.matchdays:
        for match in md.matches:
            db.delete(match)
        db.delete(md)

    # Delete all league standings associated with the season
    db.query(LeagueStanding).filter(LeagueStanding.season_id == season_id).delete()

    # Delete the season
    db.delete(season)
    db.commit()
    return

def generate_round_robin_schedule(club_ids):
    if len(club_ids) % 2 != 0:
        club_ids.append(None)

    n = len(club_ids)
    first_half = []

    for round_idx in range(n - 1):
        round_matches = []
        for i in range(n // 2):
            home = club_ids[i]
            away = club_ids[n - 1 - i]
            if home is not None and away is not None:
                round_matches.append((home, away))
        random.shuffle(round_matches)
        first_half.append(round_matches)
        club_ids = [club_ids[0]] + [club_ids[-1]] + club_ids[1:-1]

    second_half = [[(away, home) for (home, away) in round_matches] for round_matches in first_half]
    return first_half + second_half
