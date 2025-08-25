from typing import List, Optional
from pydantic import BaseModel
from typing import Literal


class SeasonCreate(BaseModel):
    name: str
    start_year: int


class MatchdaySchema(BaseModel):
    id: int
    number: int
    is_completed: bool

    class Config:
        orm_mode = True

class SeasonResponse(BaseModel):
    id: int
    name: str
    is_current: bool
    current_matchday: int
    matchdays: List[MatchdaySchema] = []

    class Config:
        orm_mode = True
