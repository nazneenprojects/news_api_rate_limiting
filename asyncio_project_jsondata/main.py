from fastapi import FastAPI
from api import router


app = FastAPI(
    title="users-api-json-demo",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
async def status_check():
    return{"message": "API is working!"}