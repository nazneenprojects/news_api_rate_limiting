from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from db.database import Base
import uuid


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)

    # Storing tags as ARRAY type (PostgreSQL specific)
    # If using SQLite, you'd need a different approach like a separate table
    tags = Column(ARRAY(String), nullable=True)

    @classmethod
    async def get_by_id(cls, db, item_id):
        """Get item by ID"""
        query = db.query(cls).filter(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db, skip=0, limit=100):
        """Get all items with pagination"""
        query = db.query(cls).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def create(cls, db, **kwargs):
        """Create a new item"""
        item = cls(**kwargs)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @classmethod
    async def update(cls, db, item_id, **kwargs):
        """Update an item"""
        query = db.query(cls).filter(cls.id == item_id)
        result = await db.execute(query)
        item = result.scalars().first()
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            await db.commit()
            await db.refresh(item)
        return item

    @classmethod
    async def delete(cls, db, item_id):
        """Delete an item"""
        query = db.query(cls).filter(cls.id == item_id)
        result = await db.execute(query)
        item = result.scalars().first()
        if item:
            await db.delete(item)
            await db.commit()
        return item