# app/schemas/financial_log_schema.py

from pydantic import BaseModel
from datetime import datetime

class FinancialLogCreate(BaseModel):
    club_id: int
    amount: float
    type: str
    description: str | None = None

class FinancialLogOut(BaseModel):
    id: int
    club_id: int
    amount: float
    type: str
    description: str | None
    timestamp: datetime

model_config = {"from_attributes": True}
