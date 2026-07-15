from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_employees: int

    active_employees: int

    total_seats: int

    occupied_seats: int

    available_seats: int

    reserved_seats: int

    maintenance_seats: int

    pending_allocations: int

    seat_utilization_percentage: float


class ProjectUtilizationItem(BaseModel):
    project_id: int

    project_name: str

    total_employees: int

    allocated_employees: int

    pending_employees: int

    occupied_seats: int

    allocation_percentage: float


class ProjectUtilizationResponse(BaseModel):
    items: list[ProjectUtilizationItem]

    total_projects: int


class FloorUtilizationItem(BaseModel):
    floor: int

    total_seats: int

    occupied_seats: int

    available_seats: int

    reserved_seats: int

    maintenance_seats: int

    occupancy_percentage: float


class FloorUtilizationResponse(BaseModel):
    items: list[FloorUtilizationItem]

    total_floors: int