from datetime import datetime
from pydantic import BaseModel # type: ignore
from typing import List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class ShrimpQuantityCreate(BaseModel):
    quantity: float
    user_id: int

class ShrimpQuantityRead(BaseModel):
    id: int
    quantity: float
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
