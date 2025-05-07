from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    tags: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tags": ["tag1", "tag2"]
            }
        }

class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass

class ItemUpdate(BaseModel):
    """Schema for updating an item - all fields are optional"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    tags: Optional[List[str]] = None

class Item(ItemBase):
    """Schema for returning an item"""
    id: int

    class Config:
        orm_mode = True

class ItemOut(BaseModel):
    """Simplified output schema for items"""
    id: int
    name: str
    price: Optional[float] = None

    class Config:
        orm_mode = True

class ItemList(BaseModel):
    """Schema for returning a list of items"""
    items: List[Item]
    total: int