from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from src.auth.router import router as auth_router
from src.database import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(title="Smart Study Planner API", version="0.1.0", lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Smart Study Planner API is running"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="My API")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
