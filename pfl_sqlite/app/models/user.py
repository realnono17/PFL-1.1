from sqlalchemy import Column, Integer, String
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String, unique=True)
    username = Column(String)
    role = Column(String, default="manager")  # e.g. "admin", "manager"