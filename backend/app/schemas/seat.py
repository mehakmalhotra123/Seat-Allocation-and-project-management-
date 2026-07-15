from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.seat import SeatStatus


class SeatBase(BaseModel):
    floor: int = Field(
        ge=1,
    )

    zone: str = Field(
        min_length=1,
        max_length=20,
    )

    bay: str = Field(
        min_length=1,
        max_length=50,
    )

    seat_number: str = Field(
        min_length=1,
        max_length=50,
    )


class SeatCreate(SeatBase):
    status: SeatStatus = SeatStatus.AVAILABLE


class SeatResponse(SeatBase):
    id: int

    status: SeatStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SeatListResponse(BaseModel):
    items: list[SeatResponse]

    total: int

    page: int

    page_size: int

    total_pages: int