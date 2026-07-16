import re

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import Seat
from app.models.allocation import SeatAllocation


def process_ai_query(
    db: Session,
    query: str,
):
    normalized_query = query.strip().lower()

    if not normalized_query:
        return _response(
            answer="Please enter a question.",
            intent="UNKNOWN",
        )

    if _is_available_seat_query(normalized_query):
        return _handle_available_seats(
            db=db,
            query=query,
        )

    if _is_utilization_query(normalized_query):
        return _handle_project_utilization(
            db=db,
            query=query,
        )

    if _is_nearby_query(normalized_query):
        return _handle_nearby_employees(
            db=db,
            query=query,
        )

    if _is_allocation_request(normalized_query):
        return _handle_allocation_request(
            db=db,
            query=query,
        )

    if _is_project_query(normalized_query):
        return _handle_project_assignment(
            db=db,
            query=query,
        )

    if _is_seat_query(normalized_query):
        return _handle_employee_seat(
            db=db,
            query=query,
        )

    return _response(
        answer=(
            "I can help with employee seating, "
            "project assignments, available seats, "
            "nearby teammates, project seat utilization, "
            "and new joiner seat recommendations. "
            "Try asking: 'Where is my seat? My email is "
            "employee@ethara.ai'."
        ),
        intent="UNKNOWN",
    )


def _is_available_seat_query(query: str):
    return (
        "available seat" in query
        or "free seat" in query
        or "vacant seat" in query
    )


def _is_utilization_query(query: str):
    utilization_keywords = [
        "how many seats",
        "occupied for",
        "seat utilization",
        "utilization for",
        "seats occupied",
    ]

    return any(
        keyword in query
        for keyword in utilization_keywords
    )


def _is_nearby_query(query: str):
    nearby_keywords = [
        "near me",
        "near employee",
        "sitting near",
        "sit near",
        "nearby",
    ]

    return any(
        keyword in query
        for keyword in nearby_keywords
    )


def _is_allocation_request(query: str):
    return (
        "allocate" in query
        or "assign a seat" in query
        or "suggest a seat" in query
        or "recommend a seat" in query
    )


def _is_project_query(query: str):
    project_keywords = [
        "which project",
        "what project",
        "project assigned",
        "project am i",
        "assigned project",
    ]

    return any(
        keyword in query
        for keyword in project_keywords
    )


def _is_seat_query(query: str):
    seat_keywords = [
        "where is my seat",
        "where is employee",
        "where is",
        "seat",
        "seated",
        "sitting",
    ]

    return any(
        keyword in query
        for keyword in seat_keywords
    )


def _extract_email(query: str):
    match = re.search(
        r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}",
        query,
    )

    if match:
        return match.group(0).lower()

    return None


def _extract_employee_code(query: str):
    match = re.search(
        r"\b(?:emp|eth)[-_]?\d+\b",
        query,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(0).upper()

    return None


def _extract_floor(query: str):
    patterns = [
        r"floor\s*(\d+)",
        r"floor\s*number\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            query,
            flags=re.IGNORECASE,
        )

        if match:
            return int(match.group(1))

    return None


def _find_employee(
    db: Session,
    query: str,
):
    email = _extract_email(query)

    if email:
        employee = (
            db.query(Employee)
            .filter(
                func.lower(Employee.email)
                == email.lower()
            )
            .first()
        )

        if employee:
            return employee

    employee_code = _extract_employee_code(query)

    if employee_code:
        employee = (
            db.query(Employee)
            .filter(
                func.lower(Employee.employee_code)
                == employee_code.lower()
            )
            .first()
        )

        if employee:
            return employee

    cleaned_query = query.lower()

    ignored_words = {
        "where",
        "is",
        "employee",
        "seated",
        "sitting",
        "seat",
        "which",
        "what",
        "project",
        "assigned",
        "to",
        "the",
        "my",
        "am",
        "i",
        "who",
        "near",
        "me",
        "allocate",
        "a",
        "for",
        "suggest",
        "recommend",
    }

    words = re.findall(
        r"[a-zA-Z]+",
        cleaned_query,
    )

    candidate_words = [
        word
        for word in words
        if word not in ignored_words
        and len(word) >= 3
    ]

    for word in candidate_words:
        employee = (
            db.query(Employee)
            .filter(
                Employee.name.ilike(
                    f"%{word}%"
                )
            )
            .first()
        )

        if employee:
            return employee

    return None


def _find_project(
    db: Session,
    query: str,
):
    projects = db.query(Project).all()

    normalized_query = query.lower()

    for project in projects:
        if (
            project.name
            and project.name.lower()
            in normalized_query
        ):
            return project

    return None


def _get_active_allocation(
    db: Session,
    employee_id: int,
):
    return (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id
            == employee_id,
            SeatAllocation.allocation_status
            == "ACTIVE",
        )
        .first()
    )


def _handle_employee_seat(
    db: Session,
    query: str,
):
    employee = _find_employee(
        db=db,
        query=query,
    )

    if not employee:
        return _response(
            answer=(
                "I could not identify the employee. "
                "Please include an employee email or "
                "employee code, for example EMP0042."
            ),
            intent="EMPLOYEE_SEAT",
        )

    allocation = _get_active_allocation(
        db=db,
        employee_id=employee.id,
    )

    project = None

    if employee.project_id:
        project = (
            db.query(Project)
            .filter(
                Project.id
                == employee.project_id
            )
            .first()
        )

    if not allocation:
        project_text = (
            f" Their assigned project is "
            f"{project.name}."
            if project
            else ""
        )

        return _response(
            answer=(
                f"{employee.name} does not currently "
                f"have an active seat allocation."
                f"{project_text}"
            ),
            intent="EMPLOYEE_SEAT",
            data={
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "allocated": False,
                "project": (
                    project.name
                    if project
                    else None
                ),
            },
        )

    seat = (
        db.query(Seat)
        .filter(
            Seat.id == allocation.seat_id
        )
        .first()
    )

    if not seat:
        return _response(
            answer=(
                f"{employee.name} has an active "
                "allocation record, but the seat "
                "details could not be found."
            ),
            intent="EMPLOYEE_SEAT",
        )

    project_text = (
        f" The assigned project is {project.name}."
        if project
        else ""
    )

    return _response(
        answer=(
            f"{employee.name} is seated on Floor "
            f"{seat.floor}, Zone {seat.zone}, "
            f"Bay {seat.bay}, Seat "
            f"{seat.seat_number}."
            f"{project_text}"
        ),
        intent="EMPLOYEE_SEAT",
        data={
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "seat_id": seat.id,
            "seat_number": seat.seat_number,
            "floor": seat.floor,
            "zone": seat.zone,
            "bay": seat.bay,
            "project": (
                project.name
                if project
                else None
            ),
        },
    )


def _handle_project_assignment(
    db: Session,
    query: str,
):
    employee = _find_employee(
        db=db,
        query=query,
    )

    if not employee:
        return _response(
            answer=(
                "I could not identify the employee. "
                "Please provide their email or employee code."
            ),
            intent="PROJECT_ASSIGNMENT",
        )

    if not employee.project_id:
        return _response(
            answer=(
                f"{employee.name} is not currently "
                "assigned to an active project."
            ),
            intent="PROJECT_ASSIGNMENT",
            data={
                "employee_id": employee.id,
                "project": None,
            },
        )

    project = (
        db.query(Project)
        .filter(
            Project.id == employee.project_id
        )
        .first()
    )

    if not project:
        return _response(
            answer=(
                f"{employee.name} has a project "
                "reference, but the project record "
                "could not be found."
            ),
            intent="PROJECT_ASSIGNMENT",
        )

    return _response(
        answer=(
            f"{employee.name} is assigned to "
            f"Project {project.name}."
        ),
        intent="PROJECT_ASSIGNMENT",
        data={
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "project_id": project.id,
            "project": project.name,
        },
    )


def _handle_available_seats(
    db: Session,
    query: str,
):
    floor = _extract_floor(query)

    seat_query = (
        db.query(Seat)
        .filter(
            Seat.status == "AVAILABLE"
        )
    )

    if floor is not None:
        seat_query = seat_query.filter(
            Seat.floor == floor
        )

    seats = (
        seat_query
        .order_by(
            Seat.floor,
            Seat.zone,
            Seat.bay,
            Seat.seat_number,
        )
        .limit(10)
        .all()
    )

    count_query = (
        db.query(func.count(Seat.id))
        .filter(
            Seat.status == "AVAILABLE"
        )
    )

    if floor is not None:
        count_query = count_query.filter(
            Seat.floor == floor
        )

    total_available = (
        count_query.scalar() or 0
    )

    if not seats:
        location_text = (
            f" on Floor {floor}"
            if floor is not None
            else ""
        )

        return _response(
            answer=(
                f"There are no available seats"
                f"{location_text}."
            ),
            intent="AVAILABLE_SEATS",
            data={
                "floor": floor,
                "count": 0,
                "seats": [],
            },
        )

    seat_numbers = ", ".join(
        seat.seat_number
        for seat in seats
    )

    location_text = (
        f" on Floor {floor}"
        if floor is not None
        else ""
    )

    return _response(
        answer=(
            f"There are {total_available} available "
            f"seats{location_text}. "
            f"Some available seats are: "
            f"{seat_numbers}."
        ),
        intent="AVAILABLE_SEATS",
        data={
            "floor": floor,
            "count": total_available,
            "seats": [
                {
                    "id": seat.id,
                    "seat_number": (
                        seat.seat_number
                    ),
                    "floor": seat.floor,
                    "zone": seat.zone,
                    "bay": seat.bay,
                }
                for seat in seats
            ],
        },
    )


def _handle_project_utilization(
    db: Session,
    query: str,
):
    project = _find_project(
        db=db,
        query=query,
    )

    if not project:
        return _response(
            answer=(
                "I could not identify the project. "
                "Please include the project name."
            ),
            intent="PROJECT_UTILIZATION",
        )

    occupied_count = (
        db.query(
            func.count(
                SeatAllocation.id
            )
        )
        .join(
            Employee,
            Employee.id
            == SeatAllocation.employee_id,
        )
        .filter(
            Employee.project_id
            == project.id,
            SeatAllocation.allocation_status
            == "ACTIVE",
        )
        .scalar()
        or 0
    )

    return _response(
        answer=(
            f"Project {project.name} currently has "
            f"{occupied_count} occupied seats."
        ),
        intent="PROJECT_UTILIZATION",
        data={
            "project_id": project.id,
            "project": project.name,
            "occupied_seats": occupied_count,
        },
    )


def _handle_nearby_employees(
    db: Session,
    query: str,
):
    employee = _find_employee(
        db=db,
        query=query,
    )

    if not employee:
        return _response(
            answer=(
                "I could not identify the employee. "
                "Please provide an email or employee code."
            ),
            intent="NEARBY_EMPLOYEES",
        )

    allocation = _get_active_allocation(
        db=db,
        employee_id=employee.id,
    )

    if not allocation:
        return _response(
            answer=(
                f"{employee.name} does not currently "
                "have an active seat allocation."
            ),
            intent="NEARBY_EMPLOYEES",
        )

    seat = (
        db.query(Seat)
        .filter(
            Seat.id == allocation.seat_id
        )
        .first()
    )

    if not seat:
        return _response(
            answer=(
                "The employee's allocated seat "
                "could not be found."
            ),
            intent="NEARBY_EMPLOYEES",
        )

    nearby_rows = (
        db.query(
            Employee,
            Seat,
        )
        .join(
            SeatAllocation,
            SeatAllocation.employee_id
            == Employee.id,
        )
        .join(
            Seat,
            Seat.id
            == SeatAllocation.seat_id,
        )
        .filter(
            SeatAllocation.allocation_status
            == "ACTIVE",
            Seat.floor == seat.floor,
            Seat.zone == seat.zone,
            Seat.bay == seat.bay,
            Employee.id != employee.id,
        )
        .limit(5)
        .all()
    )

    if not nearby_rows:
        return _response(
            answer=(
                f"I could not find other employees "
                f"in {employee.name}'s Bay "
                f"{seat.bay}, Zone {seat.zone}, "
                f"Floor {seat.floor}."
            ),
            intent="NEARBY_EMPLOYEES",
            data={
                "employee_id": employee.id,
                "nearby_employees": [],
            },
        )

    nearby_names = ", ".join(
        row_employee.name
        for row_employee, row_seat
        in nearby_rows
    )

    return _response(
        answer=(
            f"Employees sitting near "
            f"{employee.name} include "
            f"{nearby_names}. They are in "
            f"Bay {seat.bay}, Zone {seat.zone}, "
            f"Floor {seat.floor}."
        ),
        intent="NEARBY_EMPLOYEES",
        data={
            "employee_id": employee.id,
            "floor": seat.floor,
            "zone": seat.zone,
            "bay": seat.bay,
            "nearby_employees": [
                {
                    "employee_id": (
                        row_employee.id
                    ),
                    "employee_code": (
                        row_employee.employee_code
                    ),
                    "name": row_employee.name,
                    "seat_number": (
                        row_seat.seat_number
                    ),
                }
                for row_employee, row_seat
                in nearby_rows
            ],
        },
    )


def _handle_allocation_request(
    db: Session,
    query: str,
):
    employee = _find_employee(
        db=db,
        query=query,
    )

    if not employee:
        return _response(
            answer=(
                "I could not identify the employee "
                "for seat allocation. Please provide "
                "their email or employee code."
            ),
            intent="SEAT_ALLOCATION_REQUEST",
        )

    existing_allocation = (
        _get_active_allocation(
            db=db,
            employee_id=employee.id,
        )
    )

    if existing_allocation:
        seat = (
            db.query(Seat)
            .filter(
                Seat.id
                == existing_allocation.seat_id
            )
            .first()
        )

        seat_text = (
            seat.seat_number
            if seat
            else "an active seat"
        )

        return _response(
            answer=(
                f"{employee.name} already has "
                f"{seat_text} allocated."
            ),
            intent="SEAT_ALLOCATION_REQUEST",
        )

    return _response(
        answer=(
            f"{employee.name} is eligible for seat "
            "allocation. I recommend using the Smart "
            "Allocation workflow to rank available "
            "seats by project team proximity before "
            "confirming the allocation."
        ),
        intent="SEAT_ALLOCATION_REQUEST",
        data={
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "eligible_for_allocation": True,
        },
    )


def _response(
    answer: str,
    intent: str,
    data=None,
):
    return {
        "answer": answer,
        "intent": intent,
        "data": data,
    }