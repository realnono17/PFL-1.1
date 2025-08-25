from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.club import Club
from app.models.player import Player
from app.schemas.club_schema import ClubCreate, ClubUpdate, ClubOut
from app.schemas.player_schema import PlayerOut
from app.database import get_db
from app.dependencies import require_admin

router = APIRouter(prefix="/clubs", tags=["Clubs"])

# ✅ Public: All clubs
@router.get("/", response_model=List[ClubOut])
def get_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()

# ✅ Public: Single club
@router.get("/{club_id}", response_model=ClubOut)
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).get(club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club

# ✅ Public: Players in club
@router.get("/{club_id}/players", response_model=List[PlayerOut])
def get_club_players(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).get(club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return db.query(Player).filter(Player.club_id == club_id).all()

# 🔐 Admin Only: Create club
@router.post("/", response_model=ClubOut,) #dependencies=[Depends(require_admin)])
def create_club(club: ClubCreate, db: Session = Depends(get_db)):
    db_club = Club(**club.model_dump())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club

# 🔐 Admin Only: Update club
@router.put("/{club_id}", response_model=ClubOut,) #dependencies=[Depends(require_admin)])
def update_club(club_id: int, club_update: ClubUpdate, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    for field, value in club_update.dict(exclude_unset=True).items():
        setattr(club, field, value)

    db.commit()
    db.refresh(club)
    return club

# 🔐 Admin Only: Delete club
@router.delete("/{club_id}",) #dependencies=[Depends(require_admin)])
def delete_club(club_id: int, db: Session = Depends(get_db)):
    db_club = db.query(Club).get(club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club not found")
    db.delete(db_club)
    db.commit()
    return {"detail": "Club deleted"}
