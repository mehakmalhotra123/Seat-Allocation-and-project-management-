from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.employee import EmployeeStatus


class EmployeeBase(BaseModel):
    employee_code: str = Field(
        min_length=2,
        max_length=50,
    )

    name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    department: str = Field(
        min_length=2,
        max_length=100,
    )

    role: str = Field(
        min_length=2,
        max_length=100,
    )

    joining_date: date

    project_id: int | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: EmailStr | None = None

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    role: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    joining_date: date | None = None

    status: EmployeeStatus | None = None

    project_id: int | None = None


class EmployeeResponse(EmployeeBase):
    id: int

    status: EmployeeStatus

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]

    total: int

    page: int

    page_size: int

    total_pages: int


class EmployeeDeactivateResponse(BaseModel):
    message: str

    employee_id: int

    status: EmployeeStatus