from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import Base, engine
import app.models  # noqa: F401
from app.routers.employees import router as employees_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "REST API for employee seat allocation, "
        "project mapping, and seat utilization."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees_router)

@app.get("/")
def root():
    return {
        "message": "Ethara Seat Allocation API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
    }