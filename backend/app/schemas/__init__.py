from app.schemas.employee import (
    EmployeeCreate,
    EmployeeDeactivateResponse,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectEmployeesResponse,
    ProjectListResponse,
    ProjectResponse,
)
from app.schemas.seat import (
    SeatCreate,
    SeatListResponse,
    SeatResponse,
)
from app.schemas.allocation import (
    EmployeeRecommendationInfo,
    SeatAllocateRequest,
    SeatAllocationResponse,
    SeatRecommendationListResponse,
    SeatRecommendationResponse,
    SeatReleaseRequest,
    SeatReleaseResponse,
)
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    FloorUtilizationItem,
    FloorUtilizationResponse,
    ProjectUtilizationItem,
    ProjectUtilizationResponse,
)
from app.schemas.ai import (
    AIQueryRequest,
    AIQueryResponse,
)
__all__ = [
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "EmployeeListResponse",
    "EmployeeDeactivateResponse",
    "ProjectCreate",
    "ProjectResponse",
    "ProjectListResponse",
    "ProjectEmployeesResponse",
    "SeatCreate",
    "SeatResponse",
    "SeatListResponse",

    "EmployeeRecommendationInfo",
"SeatRecommendationResponse",
"SeatRecommendationListResponse",
"SeatAllocateRequest",
"SeatAllocationResponse",
"SeatReleaseRequest",
"SeatReleaseResponse",

"DashboardSummaryResponse",
"ProjectUtilizationItem",
"ProjectUtilizationResponse",
"FloorUtilizationItem",
"FloorUtilizationResponse",

"AIQueryRequest",
"AIQueryResponse",
]