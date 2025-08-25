from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    start_year = Column(Integer)
    is_current = Column(Boolean, default=False)
    current_matchday = Column(Integer, default=1)
    matchdays = relationship("Matchday", back_populates="season", cascade="all, delete-orphan")
    competitions = relationship("Competition", back_populates="season", cascade="all, delete-orphan")


