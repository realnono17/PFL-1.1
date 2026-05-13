from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.player import Player
from app.schemas.player_schema import PlayerCreate, PlayerOut, PlayerUpdate
from app.database import get_db
from app.models.club import Club
from app.dependencies import require_admin

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=List[PlayerOut])
def get_players(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25
):
    return db.query(Player).offset(skip).limit(limit).all()


@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", response_model=PlayerOut, dependencies=[Depends(require_admin)])
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.put("/{player_id}", response_model=PlayerOut, dependencies=[Depends(require_admin)])
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    db_player = db.query(Player).get(player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    for key, value in player.model_dump().items():
        setattr(db_player, key, value)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.delete("/{player_id}", dependencies=[Depends(require_admin)])
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = db.query(Player).get(player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(db_player)
    db.commit()
    return {"detail": f"Player {player_id} deleted"}
