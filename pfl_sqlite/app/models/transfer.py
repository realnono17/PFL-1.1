from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    from_club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    to_club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    transfer_fee = Column(Integer, nullable=True)
    transfer_date = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="transfers")
    from_club = relationship("Club", foreign_keys=[from_club_id])
    to_club = relationship("Club", foreign_keys=[to_club_id])
