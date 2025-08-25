from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    focus_area = Column(String, nullable=False)
    session_date = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship placeholder – if needed:
    # club = relationship("Club", back_populates="training_sessions")
