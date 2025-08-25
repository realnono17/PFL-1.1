from pydantic import BaseModel

class MatchdayOut(BaseModel):
    id: int
    number: int
    is_completed: bool
    season_id: int

    class Config:
        from_attributes = True  # For Pydantic V2 compatibility
