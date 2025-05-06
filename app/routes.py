from fastapi import APIRouter, Request
from app.db import AsyncSessionLocal
from app.models import News
from sqlmodel import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/news")
@limiter.limit("5/day")  # 5 requests per day per IP
async def get_news(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(News).limit(20))
        news_list = result.scalars().all()
        return news_list
