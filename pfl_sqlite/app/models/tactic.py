# app/models/tactic.py

from sqlalchemy import Column, Integer, ForeignKey, String
from app.models.base import Base

class Tactic(Base):
    __tablename__ = "tactics"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), unique=True)
    formation = Column(String, nullable=False)  # e.g., "4-3-3", "3-5-2"
    instructions = Column(String)  # Optional JSON or stringified data for UI
