from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectStatus
from app.schemas.employee import EmployeeResponse


class ProjectBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    manager_name: str | None = Field(
        default=None,
        max_length=150,
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    status: ProjectStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]

    total: int


class ProjectEmployeesResponse(BaseModel):
    project: ProjectResponse

    employees: list[EmployeeResponse]

    total_employees: int

    page: int

    page_size: int

    total_pages: int