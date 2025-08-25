# app/models/finance.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from app.models.base import Base

class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), unique=True)
    budget = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    expenses = Column(Float, default=0.0)
    salary_total = Column(Float, default=0.0)
