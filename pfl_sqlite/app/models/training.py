# app/models/training.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from app.models.base import Base

class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    session_type = Column(String)  # e.g., "finishing", "stamina"
    date = Column(DateTime, default=datetime.utcnow)
    result = Column(String)  # Summary of the outcome, e.g., "+2 speed"
