from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.allocation import (
    AllocationStatus,
    SeatAllocation,
)
from app.models.employee import (
    Employee,
    EmployeeStatus,
)
from app.models.project import Project
from app.models.seat import (
    Seat,
    SeatStatus,
)


def calculate_percentage(
    value: int,
    total: int,
) -> float:
    if total == 0:
        return 0.0

    return round(
        (value / total) * 100,
        2,
    )


def get_dashboard_summary(
    db: Session,
):
    total_employees = (
        db.query(func.count(Employee.id))
        .scalar()
        or 0
    )

    active_employees = (
        db.query(func.count(Employee.id))
        .filter(
            Employee.status == EmployeeStatus.ACTIVE
        )
        .scalar()
        or 0
    )

    total_seats = (
        db.query(func.count(Seat.id))
        .scalar()
        or 0
    )

    seat_counts = (
        db.query(
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.OCCUPIED,
                        1,
                    ),
                    else_=0,
                )
            ).label("occupied"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.AVAILABLE,
                        1,
                    ),
                    else_=0,
                )
            ).label("available"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.RESERVED,
                        1,
                    ),
                    else_=0,
                )
            ).label("reserved"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.MAINTENANCE,
                        1,
                    ),
                    else_=0,
                )
            ).label("maintenance"),
        )
        .one()
    )

    occupied_seats = seat_counts.occupied or 0

    available_seats = seat_counts.available or 0

    reserved_seats = seat_counts.reserved or 0

    maintenance_seats = (
        seat_counts.maintenance or 0
    )

    active_allocated_employee_ids = (
        db.query(SeatAllocation.employee_id)
        .filter(
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE
        )
    )

    pending_allocations = (
        db.query(func.count(Employee.id))
        .filter(
            Employee.status == EmployeeStatus.ACTIVE,
            ~Employee.id.in_(
                active_allocated_employee_ids
            ),
        )
        .scalar()
        or 0
    )

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "total_seats": total_seats,
        "occupied_seats": occupied_seats,
        "available_seats": available_seats,
        "reserved_seats": reserved_seats,
        "maintenance_seats": maintenance_seats,
        "pending_allocations": pending_allocations,
        "seat_utilization_percentage": (
            calculate_percentage(
                occupied_seats,
                total_seats,
            )
        ),
    }


def get_project_utilization(
    db: Session,
):
    projects = (
        db.query(Project)
        .order_by(Project.name.asc())
        .all()
    )

    items = []

    for project in projects:
        total_employees = (
            db.query(func.count(Employee.id))
            .filter(
                Employee.project_id == project.id,
                Employee.status
                == EmployeeStatus.ACTIVE,
            )
            .scalar()
            or 0
        )

        allocated_employees = (
            db.query(
                func.count(
                    func.distinct(
                        SeatAllocation.employee_id
                    )
                )
            )
            .join(
                Employee,
                Employee.id
                == SeatAllocation.employee_id,
            )
            .filter(
                SeatAllocation.project_id
                == project.id,
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE,
                Employee.status
                == EmployeeStatus.ACTIVE,
            )
            .scalar()
            or 0
        )

        pending_employees = max(
            total_employees - allocated_employees,
            0,
        )

        occupied_seats = (
            db.query(func.count(SeatAllocation.id))
            .filter(
                SeatAllocation.project_id
                == project.id,
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE,
            )
            .scalar()
            or 0
        )

        items.append(
            {
                "project_id": project.id,
                "project_name": project.name,
                "total_employees": total_employees,
                "allocated_employees": (
                    allocated_employees
                ),
                "pending_employees": pending_employees,
                "occupied_seats": occupied_seats,
                "allocation_percentage": (
                    calculate_percentage(
                        allocated_employees,
                        total_employees,
                    )
                ),
            }
        )

    return {
        "items": items,
        "total_projects": len(items),
    }


def get_floor_utilization(
    db: Session,
):
    floor_rows = (
        db.query(
            Seat.floor.label("floor"),
            func.count(Seat.id).label(
                "total_seats"
            ),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.OCCUPIED,
                        1,
                    ),
                    else_=0,
                )
            ).label("occupied_seats"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.AVAILABLE,
                        1,
                    ),
                    else_=0,
                )
            ).label("available_seats"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.RESERVED,
                        1,
                    ),
                    else_=0,
                )
            ).label("reserved_seats"),
            func.sum(
                case(
                    (
                        Seat.status
                        == SeatStatus.MAINTENANCE,
                        1,
                    ),
                    else_=0,
                )
            ).label("maintenance_seats"),
        )
        .group_by(Seat.floor)
        .order_by(Seat.floor.asc())
        .all()
    )

    items = []

    for row in floor_rows:
        total_seats = row.total_seats or 0

        occupied_seats = row.occupied_seats or 0

        items.append(
            {
                "floor": row.floor,
                "total_seats": total_seats,
                "occupied_seats": occupied_seats,
                "available_seats": (
                    row.available_seats or 0
                ),
                "reserved_seats": (
                    row.reserved_seats or 0
                ),
                "maintenance_seats": (
                    row.maintenance_seats or 0
                ),
                "occupancy_percentage": (
                    calculate_percentage(
                        occupied_seats,
                        total_seats,
                    )
                ),
            }
        )

    return {
        "items": items,
        "total_floors": len(items),
    }