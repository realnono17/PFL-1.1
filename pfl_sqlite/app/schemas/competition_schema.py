from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompetitionSchema(BaseModel):
    id: int
    name: str
    type: str
    season_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
