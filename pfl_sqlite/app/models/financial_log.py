from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from .base import Base  # <-- updated import
from sqlalchemy.orm import relationship  # <-- this one is missing!

class FinancialLog(Base):
    __tablename__ = "financial_logs"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


    club = relationship("Club", back_populates="financial_logs", lazy="noload")
