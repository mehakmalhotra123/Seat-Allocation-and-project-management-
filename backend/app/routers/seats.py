from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.seat import SeatStatus
from app.schemas.allocation import (
    SeatAllocateRequest,
    SeatAllocationResponse,
    SeatRecommendationListResponse,
    SeatReleaseRequest,
    SeatReleaseResponse,
)
from app.schemas.seat import (
    SeatCreate,
    SeatListResponse,
    SeatResponse,
)
from app.services.allocation_service import (
    allocate_seat,
    recommend_seats,
    release_seat,
)
from app.services.seat_service import (
    create_seat,
    get_available_seats,
    get_seats,
)


router = APIRouter(
    prefix="/seats",
    tags=["Seats"],
)


@router.post(
    "",
    response_model=SeatResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_seat_endpoint(
    seat_data: SeatCreate,
    db: Session = Depends(get_db),
):
    return create_seat(
        db,
        seat_data,
    )


@router.get(
    "/available",
    response_model=SeatListResponse,
)
def list_available_seats_endpoint(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    floor: int | None = Query(
        default=None,
        ge=1,
    ),
    zone: str | None = Query(
        default=None,
    ),
    bay: str | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    return get_available_seats(
        db=db,
        page=page,
        page_size=page_size,
        floor=floor,
        zone=zone,
        bay=bay,
    )


@router.get(
    "/recommend/{employee_id}",
    response_model=SeatRecommendationListResponse,
)
def recommend_seats_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return recommend_seats(
        db,
        employee_id,
    )


@router.post(
    "/allocate",
    response_model=SeatAllocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def allocate_seat_endpoint(
    allocation_data: SeatAllocateRequest,
    db: Session = Depends(get_db),
):
    return allocate_seat(
        db=db,
        employee_id=allocation_data.employee_id,
        seat_id=allocation_data.seat_id,
    )


@router.post(
    "/release",
    response_model=SeatReleaseResponse,
)
def release_seat_endpoint(
    release_data: SeatReleaseRequest,
    db: Session = Depends(get_db),
):
    return release_seat(
        db=db,
        employee_id=release_data.employee_id,
    )


@router.get(
    "",
    response_model=SeatListResponse,
)
def list_seats_endpoint(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    floor: int | None = Query(
        default=None,
        ge=1,
    ),
    zone: str | None = Query(
        default=None,
    ),
    bay: str | None = Query(
        default=None,
    ),
    seat_status: SeatStatus | None = Query(
        default=None,
        alias="status",
    ),
    project_id: int | None = Query(
        default=None,
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    return get_seats(
        db=db,
        page=page,
        page_size=page_size,
        floor=floor,
        zone=zone,
        bay=bay,
        seat_status=seat_status,
        project_id=project_id,
    )