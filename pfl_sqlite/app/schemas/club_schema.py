from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.player_schema import PlayerOut


class ClubBase(BaseModel):
    name: str
    is_controlled_by_player: Optional[bool] = False
    league: Optional[str] = "PFL1"

    founded_year: Optional[int] = None
    stadium_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    manager_name: Optional[str] = None
    trophies_won: Optional[int] = 0
    transfer_budget: Optional[float] = 0.0
    wage_budget: Optional[float] = 0.0


class ClubCreate(ClubBase):
    pass


class ClubUpdate(ClubBase):
    pass


class ClubShort(ClubBase):
    id: int

    class Config:
        from_attributes = True


class ClubOut(ClubBase):
    id: int
    players: Optional[List[PlayerOut]] = []

    class Config:
        from_attributes = True
