import os
from datetime import datetime

import httpx

from app.db import AsyncSessionLocal
from app.models import News

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


async def fetch_and_store_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=20&apiKey={NEWS_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    articles = data.get("articles", [])

    async with AsyncSessionLocal() as session:
        for article in articles:
            source_name = article.get("source", {}).get("name", "Unknown")
            news_item = News(
                title=article["title"],
                description=article.get("description"),
                url=article["url"],
                published_at=datetime.fromisoformat(article["publishedAt"].rstrip("Z")),
                source=source_name
            )
            session.add(news_item)
        await session.commit()
