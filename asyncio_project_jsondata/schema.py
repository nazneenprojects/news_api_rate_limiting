from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_active: bool

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True

class UserResponse(BaseModel):
    users: List[User]
    count: int
