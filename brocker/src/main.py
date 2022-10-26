import uvicorn
from fastapi import FastAPI

from src.producer import router

app = FastAPI(
    title="Meme twitter",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
