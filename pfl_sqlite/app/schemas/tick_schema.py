from pydantic import BaseModel

class TickResult(BaseModel):
    season_id: int
    matchday_completed: int
    message: str
