from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.competition_schema import CompetitionSchema  # import this at the top



class MatchBase(BaseModel):
    season_id: int
    home_club_id: int
    away_club_id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    competition: Optional[CompetitionSchema]
    match_date: Optional[datetime]
    matchday_id: int  # 👈 Add this


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class MatchOut(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
