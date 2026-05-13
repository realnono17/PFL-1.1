from pydantic import BaseModel
from typing import Optional

class LeagueStandingOut(BaseModel):
    id: int
    season_id: int
    competition_id: int
    club_id: int
    points: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    club_name: Optional[str]

model_config = {"from_attributes": True}