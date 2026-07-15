import enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class SeatStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    MAINTENANCE = "MAINTENANCE"


class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint(
            "floor",
            "zone",
            "seat_number",
            name="uq_seat_floor_zone_number",
        ),
        Index(
            "ix_seats_floor_zone_status",
            "floor",
            "zone",
            "status",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    floor = Column(
        Integer,
        nullable=False,
        index=True,
    )

    zone = Column(
        String(20),
        nullable=False,
        index=True,
    )

    bay = Column(
        String(50),
        nullable=False,
        index=True,
    )

    seat_number = Column(
        String(50),
        nullable=False,
    )

    status = Column(
        Enum(SeatStatus),
        nullable=False,
        default=SeatStatus.AVAILABLE,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    allocations = relationship(
        "SeatAllocation",
        back_populates="seat",
    )