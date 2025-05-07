from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import asyncio

from schema.schema import Item, ItemOut, ItemCreate, ItemUpdate, ItemList
from model.model import Item as ItemModel
from db.database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=ItemList)
async def read_items(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """
    Fetch all items with pagination
    """
    # Execute the query to get items with pagination
    result = await db.execute(select(ItemModel).offset(skip).limit(limit))
    items = result.scalars().all()

    # Count total items (for pagination info)
    result = await db.execute(select(ItemModel))
    total_items = len(result.scalars().all())

    return {"items": items, "total": total_items}


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a specific item by ID
    """
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalars().first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new item
    """
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=Item)
async def update_item(
        item_id: int,
        item: ItemUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    Update an existing item
    """
    # Get the existing item
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    db_item = result.scalars().first()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update item attributes
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", response_model=Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an item
    """
    # Get the existing item
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    db_item = result.scalars().first()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Delete the item
    await db.delete(db_item)
    await db.commit()

    return db_item


@router.get("/concurrent/{count}", response_model=List[ItemOut])
async def get_items_concurrently(count: int, db: AsyncSession = Depends(get_db)):
    """
    Demonstrates concurrent fetching of multiple items
    """

    # Create a list of tasks to fetch items concurrently
    async def fetch_item(item_id):
        result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
        return result.scalars().first()

    # Create tasks for fetching items with IDs from 1 to count
    tasks = [fetch_item(i) for i in range(1, count + 1)]

    # Wait for all tasks to complete concurrently
    items = await asyncio.gather(*tasks)

    # Filter out None values (items that don't exist)
    return [item for item in items if item is not None]