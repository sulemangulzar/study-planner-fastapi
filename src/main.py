from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.users.models import User

from .database import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(title="Smart Study Planner API", version="0.1.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Smart Study Planner API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
