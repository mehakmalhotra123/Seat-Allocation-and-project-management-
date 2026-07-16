import random
from datetime import date, timedelta

from faker import Faker

from app.database.database import Base, SessionLocal, engine
from app.models import (
    AllocationStatus,
    Employee,
    EmployeeStatus,
    Project,
    ProjectStatus,
    Seat,
    SeatAllocation,
    SeatStatus,
)


RANDOM_SEED = 42

TOTAL_EMPLOYEES = 5000
TOTAL_ALLOCATED_EMPLOYEES = 4800

TOTAL_AVAILABLE_SEATS = 550
TOTAL_RESERVED_SEATS = 100
TOTAL_MAINTENANCE_SEATS = 50


PROJECT_NAMES = [
    "Indigo",
    "Indreed",
    "Mydreed",
    "Preed",
    "Serfy",
    "Oreed",
    "bedegreed",
    "Opreed",
    "Serry",
    "Kaary",
    "Mered",
]


DEPARTMENTS = [
    "Engineering",
    "Product",
    "Design",
    "Quality Assurance",
    "Operations",
    "Growth",
    "Human Resources",
    "Finance",
    "Customer Success",
]


ROLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "QA Engineer",
    "Product Analyst",
    "Product Manager",
    "UI/UX Designer",
    "Operations Executive",
    "Growth Associate",
    "Team Lead",
]


FLOOR_ZONE_MAPPING = {
    1: ["A", "B"],
    2: ["C", "D"],
    3: ["E", "F"],
    4: ["G", "H"],
    5: ["I", "J"],
}


def reset_database():
    print("Resetting database...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Database reset complete.")


def create_projects(db):
    print("Creating projects...")

    projects = []

    for index, project_name in enumerate(PROJECT_NAMES, start=1):
        project = Project(
            name=project_name,
            description=f"{project_name} project team",
            manager_name=f"Project Manager {index}",
            status=ProjectStatus.ACTIVE,
        )

        projects.append(project)

    db.add_all(projects)
    db.commit()

    for project in projects:
        db.refresh(project)

    print(f"Created {len(projects)} projects.")

    return projects


def create_seats(db):
    print("Creating 5,500 seats...")

    seats = []

    for floor, zones in FLOOR_ZONE_MAPPING.items():
        for zone in zones:
            for bay_number in range(1, 12):
                bay = f"{zone}{bay_number}"

                for seat_index in range(1, 51):
                    seat_number = (
                        f"{zone}{bay_number}-{seat_index:02d}"
                    )

                    seat = Seat(
                        floor=floor,
                        zone=zone,
                        bay=bay,
                        seat_number=seat_number,
                        status=SeatStatus.AVAILABLE,
                    )

                    seats.append(seat)

    if len(seats) != 5500:
        raise ValueError(
            f"Expected 5,500 seats but generated {len(seats)}."
        )

    random.shuffle(seats)

    maintenance_end = TOTAL_MAINTENANCE_SEATS

    reserved_end = (
        maintenance_end + TOTAL_RESERVED_SEATS
    )

    for seat in seats[:maintenance_end]:
        seat.status = SeatStatus.MAINTENANCE

    for seat in seats[maintenance_end:reserved_end]:
        seat.status = SeatStatus.RESERVED

    db.add_all(seats)
    db.commit()

    for seat in seats:
        db.refresh(seat)

    print(f"Created {len(seats)} seats.")

    return seats


def create_employees(db, projects, fake):
    print("Creating 5,000 employees...")

    employees = []

    today = date.today()

    for employee_number in range(
        1,
        TOTAL_EMPLOYEES + 1,
    ):
        employee_code = f"EMP{employee_number:04d}"

        employee = Employee(
            employee_code=employee_code,
            name=fake.name(),
            email=(
                f"{employee_code.lower()}@ethara.ai"
            ),
            department=random.choice(DEPARTMENTS),
            role=random.choice(ROLES),
            joining_date=(
                today
                - timedelta(
                    days=random.randint(0, 1825)
                )
            ),
            status=EmployeeStatus.ACTIVE,
            project_id=random.choice(projects).id,
        )

        employees.append(employee)

    db.add_all(employees)
    db.commit()

    for employee in employees:
        db.refresh(employee)

    print(f"Created {len(employees)} employees.")

    return employees


def create_allocations(db, employees, seats):
    print("Creating seat allocations...")

    allocatable_seats = [
        seat
        for seat in seats
        if seat.status == SeatStatus.AVAILABLE
    ]

    if len(allocatable_seats) < TOTAL_ALLOCATED_EMPLOYEES:
        raise ValueError(
            "Not enough available seats for allocation."
        )

    employees_to_allocate = employees[
        :TOTAL_ALLOCATED_EMPLOYEES
    ]

    seats_to_allocate = allocatable_seats[
        :TOTAL_ALLOCATED_EMPLOYEES
    ]

    allocations = []

    for employee, seat in zip(
        employees_to_allocate,
        seats_to_allocate,
    ):
        allocation = SeatAllocation(
            employee_id=employee.id,
            seat_id=seat.id,
            project_id=employee.project_id,
            allocation_status=AllocationStatus.ACTIVE,
        )

        seat.status = SeatStatus.OCCUPIED

        allocations.append(allocation)

    db.add_all(allocations)
    db.commit()

    print(
        f"Created {len(allocations)} active allocations."
    )

    return allocations


def print_summary(db):
    print("\n========== SEED SUMMARY ==========")

    project_count = db.query(Project).count()
    employee_count = db.query(Employee).count()
    seat_count = db.query(Seat).count()

    occupied_count = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.OCCUPIED)
        .count()
    )

    available_count = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.AVAILABLE)
        .count()
    )

    reserved_count = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.RESERVED)
        .count()
    )

    maintenance_count = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.MAINTENANCE)
        .count()
    )

    active_allocation_count = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.allocation_status
            == AllocationStatus.ACTIVE
        )
        .count()
    )

    pending_allocation_count = (
        employee_count - active_allocation_count
    )

    print(f"Projects:            {project_count}")
    print(f"Employees:           {employee_count}")
    print(f"Seats:               {seat_count}")
    print(f"Occupied Seats:      {occupied_count}")
    print(f"Available Seats:     {available_count}")
    print(f"Reserved Seats:      {reserved_count}")
    print(f"Maintenance Seats:   {maintenance_count}")
    print(f"Active Allocations:  {active_allocation_count}")
    print(f"Pending Allocation:  {pending_allocation_count}")

    print("==================================\n")


def main():
    random.seed(RANDOM_SEED)

    fake = Faker()
    Faker.seed(RANDOM_SEED)

    reset_database()

    db = SessionLocal()

    try:
        projects = create_projects(db)

        seats = create_seats(db)

        employees = create_employees(
            db,
            projects,
            fake,
        )

        create_allocations(
            db,
            employees,
            seats,
        )

        print_summary(db)

    except Exception as error:
        db.rollback()

        print("Seed failed.")
        print(f"Error: {error}")

        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()

def seed_database():
    random.seed(RANDOM_SEED)

    fake = Faker()
    Faker.seed(RANDOM_SEED)

    db = SessionLocal()

    try:
        # Database already contains data
        if db.query(Employee).count() > 0:
            print("Database already seeded.")
            return

        print("Starting database seed...")

        projects = create_projects(db)

        seats = create_seats(db)

        employees = create_employees(
            db,
            projects,
            fake,
        )

        create_allocations(
            db,
            employees,
            seats,
        )

        print_summary(db)

        print("Database seeded successfully!")

    except Exception as error:
        db.rollback()

        print(f"Seed failed: {error}")

        raise

    finally:
        db.close()


if __name__ == "__main__":
    reset_database()
    seed_database()
    