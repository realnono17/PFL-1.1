from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
from datetime import datetime

class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    detail = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    performed_by = Column(String, nullable=False)  # Admin username or ID
