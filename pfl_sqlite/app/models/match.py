from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.models.competition import Competition

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"))
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=True)
    competition = relationship("Competition", back_populates="matches")  # ✅ good
    home_club_id = Column(Integer, ForeignKey("clubs.id"))
    away_club_id = Column(Integer, ForeignKey("clubs.id"))
    home_score = Column(Integer)
    away_score = Column(Integer)
    match_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    home_club = relationship("Club", foreign_keys=[home_club_id])
    away_club = relationship("Club", foreign_keys=[away_club_id])
    season = relationship("Season")
    matchday_id = Column(Integer, ForeignKey("matchdays.id", ondelete="CASCADE"), nullable=False)
    matchday = relationship("Matchday", back_populates="matches")

