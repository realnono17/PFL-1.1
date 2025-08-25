from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransferBase(BaseModel):
    player_id: int
    from_club_id: Optional[int]
    to_club_id: Optional[int]
    transfer_fee: Optional[int]
    transfer_date: Optional[datetime]

class TransferCreate(TransferBase):
    pass

class TransferOut(TransferBase):
    id: int

    class Config:
        from_attributes = True

class TransferUpdate(TransferBase):
    pass

class TransferInDB(TransferBase):
    id: int

    class Config:
        orm_mode = True
