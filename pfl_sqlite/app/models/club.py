from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_controlled_by_player = Column(Boolean, default=False)
    league = Column(String, default="PFL1")  # Used to group clubs for scheduling

    founded_year = Column(Integer, nullable=True)
    stadium_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    manager_name = Column(String, nullable=True)
    trophies_won = Column(Integer, default=0)
    transfer_budget = Column(Float, default=0.0)
    wage_budget = Column(Float, default=0.0)

    # Relationships
    players = relationship("Player", back_populates="club")
    # app/models/club.py (in class Club)
    financial_logs = relationship("FinancialLog", back_populates="club", cascade="all, delete-orphan")
    

    # At the very bottom of club.py
from .financial_log import FinancialLog


