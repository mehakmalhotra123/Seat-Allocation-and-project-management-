from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectEmployeesResponse,
    ProjectListResponse,
    ProjectResponse,
)
from app.services.project_service import (
    create_project,
    get_project_employees,
    get_projects,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_endpoint(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    return create_project(
        db,
        project_data,
    )


@router.get(
    "",
    response_model=ProjectListResponse,
)
def list_projects_endpoint(
    db: Session = Depends(get_db),
):
    return get_projects(db)


@router.get(
    "/{project_id}/employees",
    response_model=ProjectEmployeesResponse,
)
def list_project_employees_endpoint(
    project_id: int,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return get_project_employees(
        db=db,
        project_id=project_id,
        page=page,
        page_size=page_size,
    )