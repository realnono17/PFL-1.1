from pydantic import BaseModel
from datetime import datetime

class AdminLogBase(BaseModel):
    action: str
    detail: str
    performed_by: str

class AdminLogCreate(AdminLogBase):
    pass

class AdminLogOut(AdminLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
