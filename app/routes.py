from fastapi import APIRouter, Request
from app.db import AsyncSessionLocal
from app.models import News
from sqlmodel import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.schemas import NewsOut


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# @router.get("/news", response_model=list[NewsOut])
# @limiter.limit("5/day")
# async def get_news(request: Request):
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(select(News).limit(20))
#         news_list = result.scalars().all()
#         return news_list


@router.get("/news")
@limiter.limit("5/day")  # 5 requests per day per IP
async def get_news(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(News).order_by(News.published_at.desc()))
        news_items = result.scalars().all()

    articles = []
    for news_item in news_items:
        article = {
            "title": news_item.title,
            "source": {"name": news_item.source or "N/A"},
            "publishedAt": news_item.published_at.isoformat(),
            "url": news_item.url,
        }
        articles.append(article)

    return JSONResponse(content={"articles": articles})