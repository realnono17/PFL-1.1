from sqlalchemy.orm import Session
from app.models.player import Player
from app.schemas.player_schema import PlayerCreate, PlayerUpdate

# Get all players
def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Player).offset(skip).limit(limit).all()

# Get one player by ID
def get_player(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

# Create a player
def create_player(db: Session, player: PlayerCreate):
    db_player = Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

# Update player
def update_player(db: Session, player_id: int, player_data: PlayerUpdate):
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        return None
    for key, value in player_data.dict(exclude_unset=True).items():
        setattr(db_player, key, value)
    db.commit()
    db.refresh(db_player)
    return db_player

# Delete player
def delete_player(db: Session, player_id: int):
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
    return db_player
