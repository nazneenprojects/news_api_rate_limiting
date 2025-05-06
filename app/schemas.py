from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NewsSchema(BaseModel):
    id: int
    title: str
    url: str
    published_at: datetime
    description: Optional[str]
    source: str

    class Config:
        orm_mode = True


class NewsOut(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime

    class Config:
        orm_mode = True
