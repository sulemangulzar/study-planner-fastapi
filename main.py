import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from src.auth.router import router as auth_router
from src.database import create_all_tables
from src.goals.router import router as goals_router
from src.subjects.router import router as subjects_router
from src.tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(title="Smart Study Planner API", version="0.1.0", lifespan=lifespan)

# Simple CORS middleware for frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple middleware that adds request time to every response
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(auth_router)
app.include_router(subjects_router)
app.include_router(tasks_router)
app.include_router(goals_router)


@app.get("/")
async def root():
    return {"message": "Smart Study Planner API is running"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title="Study Planner API"
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}
