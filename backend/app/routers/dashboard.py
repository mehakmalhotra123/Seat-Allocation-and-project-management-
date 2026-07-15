from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    FloorUtilizationResponse,
    ProjectUtilizationResponse,
)
from app.services.dashboard_service import (
    get_dashboard_summary,
    get_floor_utilization,
    get_project_utilization,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary_endpoint(
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db)


@router.get(
    "/project-utilization",
    response_model=ProjectUtilizationResponse,
)
def project_utilization_endpoint(
    db: Session = Depends(get_db),
):
    return get_project_utilization(db)


@router.get(
    "/floor-utilization",
    response_model=FloorUtilizationResponse,
)
def floor_utilization_endpoint(
    db: Session = Depends(get_db),
):
    return get_floor_utilization(db)