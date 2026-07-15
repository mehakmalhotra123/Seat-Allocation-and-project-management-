from collections import Counter
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.allocation import (
    AllocationStatus,
    SeatAllocation,
)
from app.models.employee import (
    Employee,
    EmployeeStatus,
)
from app.models.project import (
    Project,
    ProjectStatus,
)
from app.models.seat import (
    Seat,
    SeatStatus,
)


def get_employee_for_allocation(
    db: Session,
    employee_id: int,
) -> Employee:
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    if employee.status != EmployeeStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive employee cannot receive a seat.",
        )

    if employee.project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Employee must be assigned to a project "
                "before seat allocation."
            ),
        )

    project = (
        db.query(Project)
        .filter(Project.id == employee.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee project not found.",
        )

    if project.status != ProjectStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Employee belongs to an inactive project."
            ),
        )

    return employee


def get_active_employee_allocation(
    db: Session,
    employee_id: int,
) -> SeatAllocation | None:
    return (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id == employee_id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .first()
    )


def recommend_seats(
    db: Session,
    employee_id: int,
):
    employee = get_employee_for_allocation(
        db,
        employee_id,
    )

    existing_allocation = (
        get_active_employee_allocation(
            db,
            employee_id,
        )
    )

    if existing_allocation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Employee already has an active "
                "seat allocation."
            ),
        )

    project = (
        db.query(Project)
        .filter(Project.id == employee.project_id)
        .first()
    )

    project_allocations = (
        db.query(Seat)
        .join(
            SeatAllocation,
            SeatAllocation.seat_id == Seat.id,
        )
        .filter(
            SeatAllocation.project_id
            == employee.project_id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .all()
    )

    bay_counts = Counter()

    zone_counts = Counter()

    floor_counts = Counter()

    for seat in project_allocations:
        bay_key = (
            seat.floor,
            seat.zone,
            seat.bay,
        )

        zone_key = (
            seat.floor,
            seat.zone,
        )

        bay_counts[bay_key] += 1

        zone_counts[zone_key] += 1

        floor_counts[seat.floor] += 1

    available_seats = (
        db.query(Seat)
        .filter(
            Seat.status == SeatStatus.AVAILABLE
        )
        .all()
    )

    if not available_seats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available seats found.",
        )

    recommendations = []

    for seat in available_seats:
        bay_key = (
            seat.floor,
            seat.zone,
            seat.bay,
        )

        zone_key = (
            seat.floor,
            seat.zone,
        )

        bay_teammates = bay_counts.get(
            bay_key,
            0,
        )

        zone_teammates = zone_counts.get(
            zone_key,
            0,
        )

        floor_teammates = floor_counts.get(
            seat.floor,
            0,
        )

        recommendation_score = (
            bay_teammates * 10
            + zone_teammates * 5
            + floor_teammates * 2
        )

        if bay_teammates > 0:
            proximity_level = "SAME_BAY"

            nearby_count = bay_teammates

            reason = (
                f"Recommended because "
                f"{bay_teammates} employees from "
                f"Project {project.name} are seated "
                f"in Bay {seat.bay}, "
                f"{zone_teammates} are in Zone "
                f"{seat.zone}, and "
                f"{floor_teammates} are on Floor "
                f"{seat.floor}."
            )

        elif zone_teammates > 0:
            proximity_level = "SAME_ZONE"

            nearby_count = zone_teammates

            reason = (
                f"Recommended because "
                f"{zone_teammates} employees from "
                f"Project {project.name} are seated "
                f"in Zone {seat.zone} on Floor "
                f"{seat.floor}."
            )

        elif floor_teammates > 0:
            proximity_level = "SAME_FLOOR"

            nearby_count = floor_teammates

            reason = (
                f"Recommended because "
                f"{floor_teammates} employees from "
                f"Project {project.name} are seated "
                f"on Floor {seat.floor}."
            )

        else:
            proximity_level = "ALTERNATE"

            nearby_count = 0

            reason = (
                "No nearby project teammates were "
                "found. This seat is an available "
                "alternate location."
            )

        recommendations.append(
            {
                "seat_id": seat.id,
                "floor": seat.floor,
                "zone": seat.zone,
                "bay": seat.bay,
                "seat_number": seat.seat_number,
                "proximity_level": proximity_level,
                "project_teammates_nearby": (
                    nearby_count
                ),
                "recommendation_score": (
                    recommendation_score
                ),
                "recommendation_reason": reason,
            }
        )

    recommendations.sort(
        key=lambda item: (
            -item["recommendation_score"],
            item["floor"],
            item["zone"],
            item["bay"],
            item["seat_number"],
        )
    )

    top_recommendations = recommendations[:5]

    return {
        "employee": {
            "id": employee.id,
            "employee_code": employee.employee_code,
            "name": employee.name,
            "project_id": project.id,
            "project_name": project.name,
        },
        "recommendations": top_recommendations,
    }


def allocate_seat(
    db: Session,
    employee_id: int,
    seat_id: int,
):
    try:
        employee = get_employee_for_allocation(
            db,
            employee_id,
        )

        existing_allocation = (
            get_active_employee_allocation(
                db,
                employee_id,
            )
        )

        if existing_allocation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Employee already has an active "
                    "seat allocation."
                ),
            )

        seat = (
            db.query(Seat)
            .filter(Seat.id == seat_id)
            .with_for_update()
            .first()
        )

        if seat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seat not found.",
            )

        if seat.status == SeatStatus.RESERVED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reserved seat cannot be allocated.",
            )

        if seat.status == SeatStatus.MAINTENANCE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Seat under maintenance cannot "
                    "be allocated."
                ),
            )

        if seat.status == SeatStatus.OCCUPIED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seat is already occupied.",
            )

        if seat.status != SeatStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seat is not available.",
            )

        active_seat_allocation = (
            db.query(SeatAllocation)
            .filter(
                SeatAllocation.seat_id == seat.id,
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE,
            )
            .first()
        )

        if active_seat_allocation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Seat already has an active "
                    "allocation."
                ),
            )

        project = (
            db.query(Project)
            .filter(
                Project.id == employee.project_id
            )
            .first()
        )

        allocation = SeatAllocation(
            employee_id=employee.id,
            seat_id=seat.id,
            project_id=employee.project_id,
            allocation_status=AllocationStatus.ACTIVE,
        )

        seat.status = SeatStatus.OCCUPIED

        db.add(allocation)

        db.flush()

        db.commit()

        db.refresh(allocation)

        db.refresh(seat)

        return {
            "allocation_id": allocation.id,
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "employee_name": employee.name,
            "project_id": project.id,
            "project_name": project.name,
            "seat_id": seat.id,
            "floor": seat.floor,
            "zone": seat.zone,
            "bay": seat.bay,
            "seat_number": seat.seat_number,
            "allocation_status": (
                allocation.allocation_status.value
            ),
            "allocation_date": (
                allocation.allocation_date
            ),
            "message": "Seat allocated successfully.",
        }

    except HTTPException:
        db.rollback()

        raise

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Seat allocation conflicts with an "
                "existing active allocation."
            ),
        ) from error

    except Exception:
        db.rollback()

        raise


def release_seat(
    db: Session,
    employee_id: int,
):
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found.",
            )

        allocation = (
            db.query(SeatAllocation)
            .filter(
                SeatAllocation.employee_id
                == employee_id,
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE,
            )
            .with_for_update()
            .first()
        )

        if allocation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Employee does not have an active "
                    "seat allocation."
                ),
            )

        seat = (
            db.query(Seat)
            .filter(Seat.id == allocation.seat_id)
            .with_for_update()
            .first()
        )

        if seat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Allocated seat not found.",
            )

        release_time = datetime.now(timezone.utc)

        allocation.allocation_status = (
            AllocationStatus.RELEASED
        )

        allocation.released_date = release_time

        seat.status = SeatStatus.AVAILABLE

        db.flush()

        db.commit()

        db.refresh(allocation)

        db.refresh(seat)

        return {
            "allocation_id": allocation.id,
            "employee_id": employee.id,
            "seat_id": seat.id,
            "seat_number": seat.seat_number,
            "allocation_status": (
                allocation.allocation_status.value
            ),
            "released_date": allocation.released_date,
            "seat_status": seat.status.value,
            "message": "Seat released successfully.",
        }

    except HTTPException:
        db.rollback()

        raise

    except Exception:
        db.rollback()

        raise