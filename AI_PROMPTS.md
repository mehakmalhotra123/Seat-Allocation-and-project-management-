# AI_PROMPTS.md

# Ethara Seat Allocation & Project Mapping System

This document records the AI prompts used during the development of the project, how the generated code was validated, and the manual improvements made.

---

# Prompt 1 – Project Architecture

## Prompt Used

Design a production-ready full-stack application called **Ethara Seat Allocation & Project Mapping System** using React, FastAPI, SQLAlchemy, and PostgreSQL. The system should manage employee seat allocation, project mapping, dashboard analytics, and an AI-powered seat query assistant. Follow a scalable folder structure and REST API architecture.

### AI Generated Correctly

- Suggested a modular folder structure.
- Recommended separating frontend and backend.
- Suggested service-based backend architecture.
- Recommended REST API design.

### Manual Changes

- Adjusted folder names to match the project.
- Added separate services for dashboard, employees, projects, seats, and AI.
- Organized routers and schemas.

### Validation

- Verified that the backend started successfully.
- Verified API routing using Swagger.

---

# Prompt 2 – Database Design

## Prompt Used

Design a normalized relational database for an employee seat allocation system.

Entities:

- Employees
- Projects
- Seats
- Seat Allocations

Include foreign keys, constraints, and relationships.

### AI Generated Correctly

- Suggested four-table normalized schema.
- Recommended foreign keys.
- Recommended preventing duplicate employee emails.
- Recommended one active seat allocation per employee.

### Manual Changes

- Added project relationship.
- Added seat status.
- Added allocation status.
- Added timestamps.

### Validation

- Verified database tables.
- Inserted seed data.
- Tested CRUD operations.

---

# Prompt 3 – Backend APIs

## Prompt Used

Create REST APIs using FastAPI for:

- Employees
- Projects
- Seats
- Dashboard
- Seat Allocation

Follow REST standards and SQLAlchemy best practices.

### AI Generated Correctly

- CRUD APIs
- Dependency injection
- SQLAlchemy session usage
- Response schemas

### Manual Changes

- Added dashboard endpoints.
- Added recommendation endpoint.
- Added validation logic.

### Validation

- Tested all APIs using Swagger.
- Verified HTTP status codes.

---

# Prompt 4 – Seat Allocation Logic

## Prompt Used

Implement smart seat allocation logic.

Requirements:

- One employee → one active seat
- One seat → one employee
- Reserved seats cannot be allocated
- Suggest nearby seats for the same project
- Recommend alternate zones if required

### AI Generated Correctly

- Prevented duplicate allocation.
- Checked seat availability.
- Suggested nearby seats.

### Manual Changes

- Improved recommendation scoring.
- Added fallback suggestions.

### Validation

- Tested multiple allocations.
- Verified occupied seats.
- Verified release operation.

---

# Prompt 5 – Dashboard

## Prompt Used

Create dashboard APIs returning:

- Total employees
- Total seats
- Occupied seats
- Available seats
- Reserved seats
- Floor utilization
- Project utilization
- Pending allocations

### AI Generated Correctly

- Aggregate SQL queries
- Dashboard summary endpoint

### Manual Changes

- Added charts.
- Improved response format.

### Validation

- Compared dashboard with database counts.
- Verified chart values.

---

# Prompt 6 – Frontend Dashboard

## Prompt Used

Create a responsive admin dashboard using React and Tailwind CSS.

Pages:

- Dashboard
- Employees
- Projects
- Seats
- Allocation
- AI Assistant

### AI Generated Correctly

- Responsive layout
- Sidebar
- Cards
- Tables
- Search UI

### Manual Changes

- Improved spacing.
- Added loading states.
- Added responsive behavior.
- Fixed routing.

### Validation

- Tested desktop.
- Tested tablet.
- Tested mobile.

---

# Prompt 7 – AI Assistant

## Prompt Used

Build an AI assistant for the Ethara Seat Allocation System.

The assistant should answer questions like:

- Where is EMP0001 seated?
- Which project is EMP0001 assigned to?
- Show available seats on Floor 3.
- Who is sitting near EMP0001?
- Seat utilization for Indigo.

Use FastAPI backend with a rule-based intent parser.

### AI Generated Correctly

- Intent detection.
- Query parsing.
- Response formatting.
- Backend endpoint.
- React chat UI.

### Manual Changes

- Improved UI.
- Added suggested questions.
- Added typing indicator.
- Improved error handling.

### Validation

Tested:

- Seat lookup
- Project lookup
- Available seats
- Project utilization
- Nearby employees

---

# Prompt 8 – Testing

## Prompt Used

Generate test cases for all APIs including:

- Employee CRUD
- Project CRUD
- Seat CRUD
- Dashboard
- AI Assistant
- Allocation

### AI Generated Correctly

- CRUD test scenarios
- Error cases
- Validation cases

### Manual Changes

- Added manual Swagger testing.
- Tested allocation conflicts.

### Validation

Verified all endpoints returned expected responses.

---

# Prompt 9 – Debugging

## Prompt Used

Help debug FastAPI import errors, SQLAlchemy relationship errors, React routing errors, CORS issues, and API integration problems.

### AI Generated Correctly

- Import fixes
- API fixes
- React fixes
- Routing fixes

### Manual Changes

- Corrected model imports.
- Fixed frontend routes.
- Fixed API endpoint paths.

### Validation

Verified backend startup.
Verified frontend compilation.
Verified API communication.

---

# Prompt 10 – Deployment

## Prompt Used

Deploy the application.

Frontend:
Vercel

Backend:
Render

Database:
PostgreSQL

Include environment variables and deployment configuration.

### AI Generated Correctly

- Environment variable setup
- Deployment steps
- Build commands

### Manual Changes

- Updated API URLs.
- Added production environment variables.

### Validation

Verified deployed frontend.
Verified deployed backend.
Verified API communication.

---

# Prompt 11 – Refactoring

## Prompt Used

Refactor the project to improve readability, maintainability, and scalability.

### AI Generated Correctly

- Better folder structure.
- Cleaner services.
- Reusable React components.

### Manual Changes

- Simplified component hierarchy.
- Improved naming conventions.
- Removed duplicate code.

### Validation

Verified project functionality after refactoring.

---

# What AI Generated Correctly

- Initial project architecture
- Folder structure
- Database schema suggestions
- FastAPI CRUD APIs
- SQLAlchemy models
- Dashboard APIs
- React dashboard layout
- AI assistant structure
- Error handling suggestions
- Deployment guidance

---

# What AI Generated Incorrectly

- Some SQLAlchemy imports required correction.
- Some model names differed from the project.
- Some API routes required modification.
- A few frontend components needed manual fixes.
- AI-generated status values did not always match the database.

---

# What I Manually Fixed

- Corrected SQLAlchemy model imports.
- Updated API endpoints.
- Improved seat recommendation logic.
- Fixed frontend routing.
- Improved responsive layout.
- Added loading states.
- Connected frontend with backend APIs.
- Verified database relationships.

---

# How I Verified Correctness

The project was validated by:

- Running the backend locally using FastAPI.
- Running the React frontend.
- Testing APIs using Swagger.
- Verifying CRUD operations.
- Testing seat allocation.
- Testing dashboard analytics.
- Testing AI assistant queries.
- Checking database records.
- Verifying responsive UI.

---

# AI Tools Used

- ChatGPT
- GitHub Copilot (optional)
- VS Code IntelliSense

---

# Development Stack

## Frontend

- React
- Tailwind CSS
- Axios
- React Router

## Backend

- FastAPI
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL / SQLite

## Deployment

- Vercel
- Render

---

# Conclusion

AI accelerated development by generating boilerplate code, suggesting architecture, and assisting with debugging. All generated code was manually reviewed, tested, and modified where necessary to ensure correctness and compliance with the project requirements.