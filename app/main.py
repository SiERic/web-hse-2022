from fastapi import FastAPI

from app.routers import router

app = FastAPI(
    title="App",
    description=("App"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router)
