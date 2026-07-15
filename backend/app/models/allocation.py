import enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class AllocationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RELEASED = "RELEASED"


class SeatAllocation(Base):
    __tablename__ = "seat_allocations"

    __table_args__ = (
        Index(
            "ix_allocations_employee_status",
            "employee_id",
            "allocation_status",
        ),
        Index(
            "ix_allocations_seat_status",
            "seat_id",
            "allocation_status",
        ),
        Index(
            "ix_allocations_project_status",
            "project_id",
            "allocation_status",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True,
    )

    seat_id = Column(
        Integer,
        ForeignKey("seats.id"),
        nullable=False,
        index=True,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    allocation_status = Column(
        Enum(AllocationStatus),
        nullable=False,
        default=AllocationStatus.ACTIVE,
        index=True,
    )

    allocation_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    released_date = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    employee = relationship(
        "Employee",
        back_populates="allocations",
    )

    seat = relationship(
        "Seat",
        back_populates="allocations",
    )

    project = relationship(
        "Project",
        back_populates="allocations",
    )