import asyncio
from typing import List, Optional
from fastapi import APIRouter, Depends, Query

import schema
from model import DataModel

router = APIRouter()

# Create model instance
data_model = DataModel()


# Helper function to get the data model
async def get_data_model():
    await data_model.ensure_data_loaded()
    return data_model


@router.get("/users", response_model=schema.UserResponse)
async def get_users(
        data_model: DataModel = Depends(get_data_model)):
    users = await data_model.get_users()


    return {"users": users, "count": len(users)}


@router.get("/concurrent-demo", response_model=List[schema.User])
async def concurrent_demo(data_model: DataModel = Depends(get_data_model)):
    """
    Demonstrate concurrent data fetching with asyncio.
    This endpoint fetches all users concurrently.
    """
    # Get all user IDs
    users = await data_model.get_users()
    user_ids = [user["id"] for user in users]

    # Create tasks for each user
    tasks = [data_model.get_user(user_id) for user_id in user_ids]

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    return [user for user in results if user is not None]
