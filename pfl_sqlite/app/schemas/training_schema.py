# app/schemas/training_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import List


class TrainingSessionBase(BaseModel):
    club_id: int
    player_ids: List[int]
    focus_area: str  # e.g. "speed", "passing", "strength"
    session_date: datetime


class TrainingSessionCreate(TrainingSessionBase):
    pass


class TrainingSessionUpdate(BaseModel):
    focus_area: str


class TrainingSessionOut(TrainingSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
