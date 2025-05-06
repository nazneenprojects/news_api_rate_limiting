from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    url: str
    published_at: datetime
