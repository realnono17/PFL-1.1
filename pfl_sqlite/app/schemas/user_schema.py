from pydantic import BaseModel

class UserBase(BaseModel):
    discord_id: str
    username: str
    role: str = "manager"

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True