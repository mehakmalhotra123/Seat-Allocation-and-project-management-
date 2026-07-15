import re
from collections import Counter

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.allocation import (
    AllocationStatus,
    SeatAllocation,
)
from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import (
    Seat,
    SeatStatus,
)
from app.services.allocation_service import recommend_seats


INTENT_EMPLOYEE_SEAT = "EMPLOYEE_SEAT"

INTENT_PROJECT_ASSIGNMENT = "PROJECT_ASSIGNMENT"

INTENT_AVAILABLE_SEATS = "AVAILABLE_SEATS"

INTENT_PROJECT_UTILIZATION = "PROJECT_UTILIZATION"

INTENT_TEAM_LOCATION = "TEAM_LOCATION"

INTENT_NEARBY_EMPLOYEES = "NEARBY_EMPLOYEES"

INTENT_ALLOCATE_SEAT = "ALLOCATE_SEAT"

INTENT_HELP = "HELP"

INTENT_UNKNOWN = "UNKNOWN"


def normalize_query(
    query: str,
) -> str:
    return " ".join(
        query.strip().split()
    )


def detect_intent(
    query: str,
) -> str:
    query_lower = query.lower()

    if (
        "allocate" in query_lower
        and "seat" in query_lower
    ):
        return INTENT_ALLOCATE_SEAT

    if (
        "who is sitting near" in query_lower
        or "who sits near" in query_lower
        or "near me" in query_lower
        or "near employee" in query_lower
    ):
        return INTENT_NEARBY_EMPLOYEES

    if (
        "available seat" in query_lower
        or "free seat" in query_lower
        or (
            "show" in query_lower
            and "seat" in query_lower
            and "available" in query_lower
        )
    ):
        return INTENT_AVAILABLE_SEATS

    if (
        "how many seats" in query_lower
        or "seat utilization" in query_lower
        or "seats occupied" in query_lower
        or "occupied seats" in query_lower
    ):
        return INTENT_PROJECT_UTILIZATION

    if (
        "team sitting" in query_lower
        or "team seated" in query_lower
        or "team location" in query_lower
        or (
            "where" in query_lower
            and "team" in query_lower
        )
    ):
        return INTENT_TEAM_LOCATION

    if (
        "which project" in query_lower
        or "what project" in query_lower
        or "project am i" in query_lower
        or "assigned to" in query_lower
    ):
        return INTENT_PROJECT_ASSIGNMENT

    if (
        "where is my seat" in query_lower
        or "where am i seated" in query_lower
        or "where is employee" in query_lower
        or "where is" in query_lower
        and "seated" in query_lower
        or "seat location" in query_lower
    ):
        return INTENT_EMPLOYEE_SEAT

    if (
        "help" in query_lower
        or "what can you do" in query_lower
        or "examples" in query_lower
    ):
        return INTENT_HELP

    return INTENT_UNKNOWN


def extract_employee_code(
    query: str,
) -> str | None:
    match = re.search(
        r"\bEMP[\s\-]?(\d+)\b",
        query,
        re.IGNORECASE,
    )

    if not match:
        return None

    employee_number = match.group(1)

    return f"EMP{employee_number}"


def extract_email(
    query: str,
) -> str | None:
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}\b",
        query,
    )

    if not match:
        return None

    return match.group(0).lower()


def extract_floor(
    query: str,
) -> int | None:
    match = re.search(
        r"\bfloor\s+(\d+)\b",
        query,
        re.IGNORECASE,
    )

    if not match:
        return None

    return int(match.group(1))


def extract_zone(
    query: str,
) -> str | None:
    match = re.search(
        r"\bzone\s+([A-Za-z0-9]+)\b",
        query,
        re.IGNORECASE,
    )

    if not match:
        return None

    return match.group(1).upper()


def find_employee(
    db: Session,
    query: str,
) -> Employee | None:
    employee_code = extract_employee_code(
        query
    )

    if employee_code:
        employee = (
            db.query(Employee)
            .filter(
                func.upper(Employee.employee_code)
                == employee_code.upper()
            )
            .first()
        )

        if employee:
            return employee

    email = extract_email(query)

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

    return find_employee_by_name(
        db,
        query,
    )


def find_employee_by_name(
    db: Session,
    query: str,
) -> Employee | None:
    query_lower = query.lower()

    employees = (
        db.query(Employee)
        .order_by(Employee.id.asc())
        .all()
    )

    matching_employees = []

    for employee in employees:
        employee_name = employee.name.strip()

        if (
            employee_name
            and employee_name.lower()
            in query_lower
        ):
            matching_employees.append(
                employee
            )

    if not matching_employees:
        return None

    matching_employees.sort(
        key=lambda employee: len(
            employee.name
        ),
        reverse=True,
    )

    return matching_employees[0]


def find_project(
    db: Session,
    query: str,
) -> Project | None:
    projects = (
        db.query(Project)
        .order_by(Project.id.asc())
        .all()
    )

    query_lower = query.lower()

    matching_projects = []

    for project in projects:
        project_name = project.name.strip()

        if (
            project_name
            and project_name.lower()
            in query_lower
        ):
            matching_projects.append(
                project
            )

    if not matching_projects:
        return None

    matching_projects.sort(
        key=lambda project: len(
            project.name
        ),
        reverse=True,
    )

    return matching_projects[0]


def handle_employee_seat(
    db: Session,
    query: str,
):
    employee = find_employee(
        db,
        query,
    )

    if employee is None:
        return {
            "answer": (
                "I could not identify the employee. "
                "Please provide an employee code or "
                "email, for example EMP1024 or "
                "employee@ethara.ai."
            ),
            "intent": INTENT_EMPLOYEE_SEAT,
            "data": None,
        }

    allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id
            == employee.id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .first()
    )

    project = None

    if employee.project_id is not None:
        project = (
            db.query(Project)
            .filter(
                Project.id
                == employee.project_id
            )
            .first()
        )

    if allocation is None:
        return {
            "answer": (
                f"{employee.name} "
                f"({employee.employee_code}) does not "
                f"currently have an allocated seat."
            ),
            "intent": INTENT_EMPLOYEE_SEAT,
            "data": {
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "employee_name": employee.name,
                "allocated": False,
                "project_name": (
                    project.name
                    if project
                    else None
                ),
            },
        }

    seat = (
        db.query(Seat)
        .filter(
            Seat.id == allocation.seat_id
        )
        .first()
    )

    if seat is None:
        return {
            "answer": (
                "The employee has an active allocation "
                "record, but the associated seat could "
                "not be found."
            ),
            "intent": INTENT_EMPLOYEE_SEAT,
            "data": None,
        }

    project_name = (
        project.name
        if project
        else "No active project"
    )

    return {
        "answer": (
            f"{employee.name} "
            f"({employee.employee_code}) is seated on "
            f"Floor {seat.floor}, Zone {seat.zone}, "
            f"Bay {seat.bay}, Seat "
            f"{seat.seat_number}. "
            f"The assigned project is "
            f"{project_name}."
        ),
        "intent": INTENT_EMPLOYEE_SEAT,
        "data": {
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "allocated": True,
            "project_name": project_name,
            "seat_id": seat.id,
            "floor": seat.floor,
            "zone": seat.zone,
            "bay": seat.bay,
            "seat_number": seat.seat_number,
        },
    }


def handle_project_assignment(
    db: Session,
    query: str,
):
    employee = find_employee(
        db,
        query,
    )

    if employee is None:
        return {
            "answer": (
                "I could not identify the employee. "
                "Please provide an employee code or "
                "email."
            ),
            "intent": INTENT_PROJECT_ASSIGNMENT,
            "data": None,
        }

    if employee.project_id is None:
        return {
            "answer": (
                f"{employee.name} "
                f"({employee.employee_code}) is not "
                f"currently assigned to a project."
            ),
            "intent": INTENT_PROJECT_ASSIGNMENT,
            "data": {
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "project_id": None,
                "project_name": None,
            },
        }

    project = (
        db.query(Project)
        .filter(
            Project.id == employee.project_id
        )
        .first()
    )

    if project is None:
        return {
            "answer": (
                "The employee has a project reference, "
                "but the project record could not be "
                "found."
            ),
            "intent": INTENT_PROJECT_ASSIGNMENT,
            "data": None,
        }

    return {
        "answer": (
            f"{employee.name} "
            f"({employee.employee_code}) is assigned "
            f"to Project {project.name}."
        ),
        "intent": INTENT_PROJECT_ASSIGNMENT,
        "data": {
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "project_id": project.id,
            "project_name": project.name,
        },
    }


def handle_available_seats(
    db: Session,
    query: str,
):
    floor = extract_floor(query)

    zone = extract_zone(query)

    seat_query = (
        db.query(Seat)
        .filter(
            Seat.status == SeatStatus.AVAILABLE
        )
    )

    if floor is not None:
        seat_query = seat_query.filter(
            Seat.floor == floor
        )

    if zone is not None:
        seat_query = seat_query.filter(
            Seat.zone == zone
        )

    total_available = seat_query.count()

    seats = (
        seat_query
        .order_by(
            Seat.floor.asc(),
            Seat.zone.asc(),
            Seat.bay.asc(),
            Seat.seat_number.asc(),
        )
        .limit(10)
        .all()
    )

    seat_data = [
        {
            "seat_id": seat.id,
            "floor": seat.floor,
            "zone": seat.zone,
            "bay": seat.bay,
            "seat_number": seat.seat_number,
        }
        for seat in seats
    ]

    location_parts = []

    if floor is not None:
        location_parts.append(
            f"Floor {floor}"
        )

    if zone is not None:
        location_parts.append(
            f"Zone {zone}"
        )

    location_text = (
        ", ".join(location_parts)
        if location_parts
        else "all locations"
    )

    if total_available == 0:
        answer = (
            f"No available seats were found for "
            f"{location_text}."
        )

    else:
        answer = (
            f"There are {total_available} available "
            f"seats for {location_text}. "
            f"I returned up to 10 seat options."
        )

    return {
        "answer": answer,
        "intent": INTENT_AVAILABLE_SEATS,
        "data": {
            "floor": floor,
            "zone": zone,
            "total_available": total_available,
            "seats": seat_data,
        },
    }


def handle_project_utilization(
    db: Session,
    query: str,
):
    project = find_project(
        db,
        query,
    )

    if project is None:
        return {
            "answer": (
                "I could not identify the project. "
                "Please include a project name."
            ),
            "intent": INTENT_PROJECT_UTILIZATION,
            "data": None,
        }

    occupied_seats = (
        db.query(func.count(SeatAllocation.id))
        .filter(
            SeatAllocation.project_id
            == project.id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .scalar()
        or 0
    )

    total_employees = (
        db.query(func.count(Employee.id))
        .filter(
            Employee.project_id == project.id
        )
        .scalar()
        or 0
    )

    return {
        "answer": (
            f"Project {project.name} currently has "
            f"{occupied_seats} occupied seats for "
            f"{total_employees} mapped employees."
        ),
        "intent": INTENT_PROJECT_UTILIZATION,
        "data": {
            "project_id": project.id,
            "project_name": project.name,
            "occupied_seats": occupied_seats,
            "total_employees": total_employees,
        },
    }


def handle_team_location(
    db: Session,
    query: str,
):
    project = find_project(
        db,
        query,
    )

    if project is None:
        return {
            "answer": (
                "I could not identify the project. "
                "Please include a project name."
            ),
            "intent": INTENT_TEAM_LOCATION,
            "data": None,
        }

    seats = (
        db.query(Seat)
        .join(
            SeatAllocation,
            SeatAllocation.seat_id == Seat.id,
        )
        .filter(
            SeatAllocation.project_id
            == project.id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .all()
    )

    if not seats:
        return {
            "answer": (
                f"Project {project.name} does not "
                f"currently have active seat "
                f"allocations."
            ),
            "intent": INTENT_TEAM_LOCATION,
            "data": {
                "project_id": project.id,
                "project_name": project.name,
                "locations": [],
            },
        }

    bay_counts = Counter(
        (
            seat.floor,
            seat.zone,
            seat.bay,
        )
        for seat in seats
    )

    top_locations = (
        bay_counts.most_common(5)
    )

    locations = []

    for location, employee_count in top_locations:
        floor, zone, bay = location

        locations.append(
            {
                "floor": floor,
                "zone": zone,
                "bay": bay,
                "employee_count": employee_count,
            }
        )

    top_location = locations[0]

    return {
        "answer": (
            f"Project {project.name} is most "
            f"concentrated on Floor "
            f"{top_location['floor']}, Zone "
            f"{top_location['zone']}, Bay "
            f"{top_location['bay']}, where "
            f"{top_location['employee_count']} team "
            f"members are seated. I also returned "
            f"the top five team locations."
        ),
        "intent": INTENT_TEAM_LOCATION,
        "data": {
            "project_id": project.id,
            "project_name": project.name,
            "locations": locations,
        },
    }


def handle_nearby_employees(
    db: Session,
    query: str,
):
    employee = find_employee(
        db,
        query,
    )

    if employee is None:
        return {
            "answer": (
                "I could not identify the employee. "
                "Please provide an employee code or "
                "email."
            ),
            "intent": INTENT_NEARBY_EMPLOYEES,
            "data": None,
        }

    allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id
            == employee.id,
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if allocation is None:
        return {
            "answer": (
                f"{employee.name} does not currently "
                f"have an allocated seat, so I cannot "
                f"find nearby employees."
            ),
            "intent": INTENT_NEARBY_EMPLOYEES,
            "data": None,
        }

    employee_seat = (
        db.query(Seat)
        .filter(
            Seat.id == allocation.seat_id
        )
        .first()
    )

    if employee_seat is None:
        return {
            "answer": (
                "The employee seat could not be found."
            ),
            "intent": INTENT_NEARBY_EMPLOYEES,
            "data": None,
        }

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
            == AllocationStatus.ACTIVE,
            Seat.floor == employee_seat.floor,
            Seat.zone == employee_seat.zone,
            Seat.bay == employee_seat.bay,
            Employee.id != employee.id,
        )
        .order_by(
            Seat.seat_number.asc()
        )
        .limit(10)
        .all()
    )

    nearby_employees = [
        {
            "employee_id": nearby_employee.id,
            "employee_code": (
                nearby_employee.employee_code
            ),
            "name": nearby_employee.name,
            "seat_number": nearby_seat.seat_number,
        }
        for nearby_employee, nearby_seat
        in nearby_rows
    ]

    if not nearby_employees:
        answer = (
            f"No other employees are currently seated "
            f"in the same bay as {employee.name}."
        )

    else:
        answer = (
            f"I found {len(nearby_employees)} "
            f"employees in the same bay as "
            f"{employee.name}. The response includes "
            f"up to 10 nearby employees."
        )

    return {
        "answer": answer,
        "intent": INTENT_NEARBY_EMPLOYEES,
        "data": {
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "location": {
                "floor": employee_seat.floor,
                "zone": employee_seat.zone,
                "bay": employee_seat.bay,
                "seat_number": (
                    employee_seat.seat_number
                ),
            },
            "nearby_employees": nearby_employees,
        },
    }


def handle_allocate_seat(
    db: Session,
    query: str,
):
    employee = find_employee(
        db,
        query,
    )

    if employee is None:
        return {
            "answer": (
                "I could not identify the employee. "
                "Please provide an employee code or "
                "email."
            ),
            "intent": INTENT_ALLOCATE_SEAT,
            "data": None,
            "requires_confirmation": False,
        }

    try:
        recommendation_result = recommend_seats(
            db,
            employee.id,
        )

    except Exception as error:
        detail = getattr(
            error,
            "detail",
            str(error),
        )

        return {
            "answer": str(detail),
            "intent": INTENT_ALLOCATE_SEAT,
            "data": None,
            "requires_confirmation": False,
        }

    recommendations = (
        recommendation_result[
            "recommendations"
        ]
    )

    if not recommendations:
        return {
            "answer": (
                "No seat recommendation is currently "
                "available."
            ),
            "intent": INTENT_ALLOCATE_SEAT,
            "data": None,
            "requires_confirmation": False,
        }

    recommended_seat = recommendations[0]

    return {
        "answer": (
            f"I recommend Seat "
            f"{recommended_seat['seat_number']} on "
            f"Floor {recommended_seat['floor']}, "
            f"Zone {recommended_seat['zone']}, "
            f"Bay {recommended_seat['bay']} for "
            f"{employee.name}. "
            f"{recommended_seat['recommendation_reason']} "
            f"Please confirm the allocation before "
            f"the seat is assigned."
        ),
        "intent": INTENT_ALLOCATE_SEAT,
        "data": {
            "employee_id": employee.id,
            "employee_code": (
                employee.employee_code
            ),
            "employee_name": employee.name,
            "recommended_seat": recommended_seat,
            "recommendations": recommendations,
        },
        "requires_confirmation": True,
    }


def handle_help():
    return {
        "answer": (
            "I can help find employee seats, check "
            "project assignments, show available "
            "seats by floor or zone, report project "
            "seat utilization, locate project teams, "
            "find nearby employees, and recommend "
            "seats for pending employees."
        ),
        "intent": INTENT_HELP,
        "data": {
            "example_queries": [
                "Where is employee EMP1024 seated?",
                (
                    "Which project is EMP1024 "
                    "assigned to?"
                ),
                (
                    "Show available seats on Floor 3."
                ),
                (
                    "How many seats are occupied "
                    "for Indigo?"
                ),
                (
                    "Where is the Indigo team sitting?"
                ),
                (
                    "Who is sitting near EMP1024?"
                ),
                (
                    "Allocate a seat for EMP4801."
                ),
            ]
        },
    }


def process_ai_query(
    db: Session,
    query: str,
):
    normalized_query = normalize_query(
        query
    )

    intent = detect_intent(
        normalized_query
    )

    if intent == INTENT_EMPLOYEE_SEAT:
        return handle_employee_seat(
            db,
            normalized_query,
        )

    if intent == INTENT_PROJECT_ASSIGNMENT:
        return handle_project_assignment(
            db,
            normalized_query,
        )

    if intent == INTENT_AVAILABLE_SEATS:
        return handle_available_seats(
            db,
            normalized_query,
        )

    if intent == INTENT_PROJECT_UTILIZATION:
        return handle_project_utilization(
            db,
            normalized_query,
        )

    if intent == INTENT_TEAM_LOCATION:
        return handle_team_location(
            db,
            normalized_query,
        )

    if intent == INTENT_NEARBY_EMPLOYEES:
        return handle_nearby_employees(
            db,
            normalized_query,
        )

    if intent == INTENT_ALLOCATE_SEAT:
        return handle_allocate_seat(
            db,
            normalized_query,
        )

    if intent == INTENT_HELP:
        return handle_help()

    return {
        "answer": (
            "I could not understand that seat or "
            "project query. Ask 'What can you do?' "
            "to see supported examples."
        ),
        "intent": INTENT_UNKNOWN,
        "data": None,
        "requires_confirmation": False,
    }