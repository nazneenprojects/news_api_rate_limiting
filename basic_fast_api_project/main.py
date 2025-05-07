from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router
from db.database import engine
from model.model import Base


app = FastAPI(
    title="Demo API",
    description="API is made for practice",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "api is wortking!"}

origins = ["http://loccalhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables on startup
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api/v1")


