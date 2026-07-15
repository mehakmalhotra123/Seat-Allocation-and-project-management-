from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.employee import EmployeeStatus
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeDeactivateResponse,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import (
    create_employee,
    deactivate_employee,
    get_employee_by_id,
    get_employees,
    update_employee,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_endpoint(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return create_employee(
        db,
        employee_data,
    )


@router.get(
    "",
    response_model=EmployeeListResponse,
)
def list_employees_endpoint(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
    ),
    project_id: int | None = Query(
        default=None,
        ge=1,
    ),
    department: str | None = Query(
        default=None,
    ),
    employee_status: EmployeeStatus | None = Query(
        default=None,
        alias="status",
    ),
    allocated: bool | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    return get_employees(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        project_id=project_id,
        department=department,
        employee_status=employee_status,
        allocated=allocated,
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_employee_by_id(
        db,
        employee_id,
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee_endpoint(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    return update_employee(
        db,
        employee_id,
        employee_data,
    )


@router.delete(
    "/{employee_id}",
    response_model=EmployeeDeactivateResponse,
)
def deactivate_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = deactivate_employee(
        db,
        employee_id,
    )

    return {
        "message": "Employee deactivated successfully.",
        "employee_id": employee.id,
        "status": employee.status,
    }