import math

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.project import (
    Project,
    ProjectStatus,
)
from app.schemas.project import ProjectCreate


def create_project(
    db: Session,
    project_data: ProjectCreate,
) -> Project:
    normalized_name = project_data.name.strip()

    existing_project = (
        db.query(Project)
        .filter(
            Project.name.ilike(normalized_name)
        )
        .first()
    )

    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project name already exists.",
        )

    project = Project(
        name=normalized_name,
        description=(
            project_data.description.strip()
            if project_data.description
            else None
        ),
        manager_name=(
            project_data.manager_name.strip()
            if project_data.manager_name
            else None
        ),
        status=ProjectStatus.ACTIVE,
    )

    try:
        db.add(project)
        db.commit()
        db.refresh(project)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project name already exists.",
        )

    return project


def get_projects(
    db: Session,
):
    projects = (
        db.query(Project)
        .order_by(Project.name.asc())
        .all()
    )

    return {
        "items": projects,
        "total": len(projects),
    }


def get_project_by_id(
    db: Session,
    project_id: int,
) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


def get_project_employees(
    db: Session,
    project_id: int,
    page: int,
    page_size: int,
):
    project = get_project_by_id(
        db,
        project_id,
    )

    query = (
        db.query(Employee)
        .filter(Employee.project_id == project_id)
    )

    total = query.count()

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    employees = (
        query
        .order_by(Employee.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "project": project,
        "employees": employees,
        "total_employees": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }