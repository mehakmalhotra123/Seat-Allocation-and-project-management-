import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class ProjectStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    manager_name = Column(
        String(150),
        nullable=True,
    )

    status = Column(
        Enum(ProjectStatus),
        nullable=False,
        default=ProjectStatus.ACTIVE,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    employees = relationship(
        "Employee",
        back_populates="project",
    )

    allocations = relationship(
        "SeatAllocation",
        back_populates="project",
    )