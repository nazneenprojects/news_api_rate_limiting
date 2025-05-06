from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router, limiter
from slowapi.middleware import SlowAPIMiddleware
from app.db import init_db
from app.news_fetcher import fetch_and_store_news

import asyncio

app = FastAPI(title="Async - News Fetcher",
    version="v0.1.0a")

# Allow CORS from all origins for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(router)


@app.get("/")
async def root():
    return {"status": "API working"}


@app.on_event("startup")
async def startup():
    await init_db()
    # Automatically fetch news on startup
    await fetch_and_store_news()