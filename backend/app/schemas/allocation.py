from datetime import datetime

from pydantic import BaseModel, Field


class SeatRecommendationResponse(BaseModel):
    seat_id: int

    floor: int

    zone: str

    bay: str

    seat_number: str

    proximity_level: str

    project_teammates_nearby: int

    recommendation_score: int

    recommendation_reason: str


class EmployeeRecommendationInfo(BaseModel):
    id: int

    employee_code: str

    name: str

    project_id: int

    project_name: str


class SeatRecommendationListResponse(BaseModel):
    employee: EmployeeRecommendationInfo

    recommendations: list[SeatRecommendationResponse]


class SeatAllocateRequest(BaseModel):
    employee_id: int = Field(
        ge=1,
    )

    seat_id: int = Field(
        ge=1,
    )


class SeatAllocationResponse(BaseModel):
    allocation_id: int

    employee_id: int

    employee_code: str

    employee_name: str

    project_id: int

    project_name: str

    seat_id: int

    floor: int

    zone: str

    bay: str

    seat_number: str

    allocation_status: str

    allocation_date: datetime

    message: str


class SeatReleaseRequest(BaseModel):
    employee_id: int = Field(
        ge=1,
    )


class SeatReleaseResponse(BaseModel):
    allocation_id: int

    employee_id: int

    seat_id: int

    seat_number: str

    allocation_status: str

    released_date: datetime

    seat_status: str

    message: str