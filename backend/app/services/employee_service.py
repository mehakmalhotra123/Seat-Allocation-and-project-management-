import math

from fastapi import HTTPException, status
from sqlalchemy import or_
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
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
)


def validate_project(
    db: Session,
    project_id: int | None,
) -> Project | None:
    if project_id is None:
        return None

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    if project.status != ProjectStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee cannot be assigned to an inactive project.",
        )

    return project


def create_employee(
    db: Session,
    employee_data: EmployeeCreate,
) -> Employee:
    existing_email = (
        db.query(Employee)
        .filter(
            Employee.email
            == employee_data.email.lower()
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee email already exists.",
        )

    normalized_employee_code = (
        employee_data.employee_code
        .strip()
        .upper()
    )

    existing_code = (
        db.query(Employee)
        .filter(
            Employee.employee_code
            == normalized_employee_code
        )
        .first()
    )

    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists.",
        )

    validate_project(
        db,
        employee_data.project_id,
    )

    employee = Employee(
        employee_code=normalized_employee_code,
        name=employee_data.name.strip(),
        email=str(employee_data.email).lower(),
        department=employee_data.department.strip(),
        role=employee_data.role.strip(),
        joining_date=employee_data.joining_date,
        project_id=employee_data.project_id,
        status=EmployeeStatus.ACTIVE,
    )

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Employee could not be created because "
                "a unique employee field already exists."
            ),
        )

    return employee


def get_employees(
    db: Session,
    page: int,
    page_size: int,
    search: str | None = None,
    project_id: int | None = None,
    department: str | None = None,
    employee_status: EmployeeStatus | None = None,
    allocated: bool | None = None,
):
    query = db.query(Employee)

    if search:
        search_value = f"%{search.strip()}%"

        query = query.filter(
            or_(
                Employee.name.ilike(search_value),
                Employee.employee_code.ilike(
                    search_value
                ),
                Employee.email.ilike(search_value),
            )
        )

    if project_id is not None:
        query = query.filter(
            Employee.project_id == project_id
        )

    if department:
        query = query.filter(
            Employee.department.ilike(
                department.strip()
            )
        )

    if employee_status is not None:
        query = query.filter(
            Employee.status == employee_status
        )

    if allocated is True:
        query = query.filter(
            Employee.allocations.any(
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE
            )
        )

    elif allocated is False:
        query = query.filter(
            ~Employee.allocations.any(
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE
            )
        )

    total = query.count()

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    employees = (
        query
        .order_by(Employee.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": employees,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_employee_by_id(
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

    return employee


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee:
    employee = get_employee_by_id(
        db,
        employee_id,
    )

    update_data = employee_data.model_dump(
        exclude_unset=True,
    )

    if "email" in update_data:
        normalized_email = str(
            update_data["email"]
        ).lower()

        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == normalized_email,
                Employee.id != employee_id,
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee email already exists.",
            )

        update_data["email"] = normalized_email

    if "project_id" in update_data:
        validate_project(
            db,
            update_data["project_id"],
        )

    for field, value in update_data.items():
        if isinstance(value, str):
            value = value.strip()

        setattr(
            employee,
            field,
            value,
        )

    try:
        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee update violates a database constraint.",
        )

    return employee


def deactivate_employee(
    db: Session,
    employee_id: int,
) -> Employee:
    employee = get_employee_by_id(
        db,
        employee_id,
    )

    if employee.status == EmployeeStatus.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee is already inactive.",
        )

    active_allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id
            == employee_id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if active_allocation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Employee has an active seat allocation. "
                "Release the seat before deactivating "
                "the employee."
            ),
        )

    employee.status = EmployeeStatus.INACTIVE

    db.commit()
    db.refresh(employee)

    return employee