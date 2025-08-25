# app/models/matchday.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Matchday(Base):
    __tablename__ = "matchdays"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)

    season_id = Column(Integer, ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    season = relationship("Season", back_populates="matchdays")

    matches = relationship("Match", back_populates="matchday", cascade="all, delete-orphan")
