from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "league" or "cup"
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    season = relationship("Season", back_populates="competitions")  # if using
    matches = relationship("Match", back_populates="competition", cascade="all, delete-orphan")