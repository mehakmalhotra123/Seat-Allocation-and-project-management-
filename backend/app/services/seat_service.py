import math

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.allocation import (
    AllocationStatus,
    SeatAllocation,
)
from app.models.seat import (
    Seat,
    SeatStatus,
)
from app.schemas.seat import SeatCreate


def create_seat(
    db: Session,
    seat_data: SeatCreate,
) -> Seat:
    normalized_zone = (
        seat_data.zone
        .strip()
        .upper()
    )

    normalized_bay = (
        seat_data.bay
        .strip()
        .upper()
    )

    normalized_seat_number = (
        seat_data.seat_number
        .strip()
        .upper()
    )

    existing_seat = (
        db.query(Seat)
        .filter(
            Seat.floor == seat_data.floor,
            Seat.zone == normalized_zone,
            Seat.seat_number == normalized_seat_number,
        )
        .first()
    )

    if existing_seat:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Seat number already exists on "
                "the same floor and zone."
            ),
        )

    if seat_data.status == SeatStatus.OCCUPIED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "A new seat cannot be created as OCCUPIED. "
                "Use the seat allocation API."
            ),
        )

    seat = Seat(
        floor=seat_data.floor,
        zone=normalized_zone,
        bay=normalized_bay,
        seat_number=normalized_seat_number,
        status=seat_data.status,
    )

    try:
        db.add(seat)
        db.commit()
        db.refresh(seat)

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Seat number already exists on "
                "the same floor and zone."
            ),
        ) from error

    return seat


def get_seats(
    db: Session,
    page: int,
    page_size: int,
    floor: int | None = None,
    zone: str | None = None,
    bay: str | None = None,
    seat_status: SeatStatus | None = None,
    project_id: int | None = None,
):
    query = db.query(Seat)

    if floor is not None:
        query = query.filter(
            Seat.floor == floor
        )

    if zone:
        query = query.filter(
            Seat.zone == zone.strip().upper()
        )

    if bay:
        query = query.filter(
            Seat.bay == bay.strip().upper()
        )

    if seat_status is not None:
        query = query.filter(
            Seat.status == seat_status
        )

    if project_id is not None:
        query = query.filter(
            Seat.allocations.any(
                SeatAllocation.project_id == project_id,
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE,
            )
        )

    total = query.count()

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    seats = (
        query
        .order_by(
            Seat.floor.asc(),
            Seat.zone.asc(),
            Seat.bay.asc(),
            Seat.seat_number.asc(),
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": seats,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_available_seats(
    db: Session,
    page: int,
    page_size: int,
    floor: int | None = None,
    zone: str | None = None,
    bay: str | None = None,
):
    query = (
        db.query(Seat)
        .filter(
            Seat.status == SeatStatus.AVAILABLE
        )
    )

    if floor is not None:
        query = query.filter(
            Seat.floor == floor
        )

    if zone:
        query = query.filter(
            Seat.zone == zone.strip().upper()
        )

    if bay:
        query = query.filter(
            Seat.bay == bay.strip().upper()
        )

    total = query.count()

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    seats = (
        query
        .order_by(
            Seat.floor.asc(),
            Seat.zone.asc(),
            Seat.bay.asc(),
            Seat.seat_number.asc(),
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": seats,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }