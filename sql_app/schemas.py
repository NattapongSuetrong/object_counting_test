from datetime import datetime
from pydantic import BaseModel # type: ignore

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
    quantity: int
    user_id: int

class ShrimpQuantityRead(BaseModel):
    id: int
    quantity: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ShrimpPondCreate(BaseModel):
    pond_name: str
    user_id: int
    pond_quantity: int
    shrimp_sold: int

class ShrimpPondRead(BaseModel):
    id: int
    pond_name: str
    user_id: int
    pond_quantity: int
    shrimp_sold: int
    date: datetime

    class Config:
        orm_mode = True
        
class ShrimpPondUpdate(BaseModel):
    pond_name: str
    user_id: int
    pond_quantity: int
    shrimp_sold: int
    date: datetime
