
# Course Enrollment Platform API
A structured, production-ready FastAPI backend for managing users, courses,
 and student enrollments with role-based access control, business-rule enforcement, and high test coverage.

# Table of Contents
•	Purpose & Scope
•	Core Concepts
•	Architecture Overview
•	API Design
•	Authentication & Authorization
•	Business Rules
•	Project Structure
•	Installation & Setup
•	Running the Application
•	Testing Strategy
•	Coverage & Quality
•	Extensibility
•	License
________________________________________
# Purpose & Scope
The Course Enrollment Platform API provides a backend service that allows:
•	administrators to manage courses and users
•	students to enroll in available courses
•	the system to enforce real-world constraints such as:
o	course capacity limits
o	duplicate enrollment prevention
o	role-based access restrictions
o	active/inactive resource states

# Core Concepts
# Roles
•	Admin
o	create and manage courses
o	view all users and enrollments
•	Student
o	view available courses
o	enroll in active courses
o	view own enrollments

# Resources
•	User
•	Course
•	Enrollment

# Architecture Overview
The application follows a layered architecture with strict separation of concerns:
Layers
1.	Routes
o	HTTP request handling
o	dependency injection
o	response formatting
2.	Schemas
o	input validation
o	response contracts
3.	Services
o	business logic
o	rule enforcement
o	domain behavior
4.	Models
o	database structure
o	relationships
5.	Dependencies
o	authentication
o	authorization
o	database session handling

# API Design
Canonical Paths
/api/v1/auth
/api/v1/user
/api/v1/course
/api/v1/enrollment

# Authentication & Authorization
•	JWT-based authentication
•	Password hashing handled securely
•	Role-based access enforced via dependencies
•	Authorization checks are explicit and centralized


# Business Rules
The system enforces the following rules at the service layer:
•	A student cannot enroll in an inactive course
•	A student cannot enroll in a full course
•	A student cannot enroll in the same course twice
•	Admins cannot enroll as students
•	Only admins can manage courses
•	Only authorized users can access user data
All violations return appropriate HTTP status codes (403, 409, 404, etc.).

# Project Structure
app/
├── main.py                     
├── api/v1/routes/              
│   ├── auth.py
│   ├── user.py
│   ├── course.py
│   └── enrollment.py
├── core/
│   ├── config.py               
│   └── security.py             
├── db/
│   ├── base.py
│   ├── session.py
│   └── models/
│       ├── user.py
│       ├── course.py
│       └── enrollment.py
├── schemas/                    
├── services/                   
├── dependency/
│   └── deps.py                 
└── test/
    ├── conftest.py
    ├── test_auth.py
    ├── test_user.py
    ├── test_course.py
    ├── test_enrollment.py
________________________________________

# Installation & Setup
Requirements
•	Python 3.10+
•	PostgreSQL
•	pip or virtualenv
Prerequisites
•	Python 3.9+
•	PostgreSQL
•	pip
Steps
# Create virtual environment
python -m venv venv
source venv/bin/activate  
 # Windows: 
 venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt

# Run migrations:
alembic upgrade head
________________________________________
 
 # Running the Application
uvicorn app.main:app --reload
•	API: http://localhost:8000
•	Swagger UI: http://localhost:8000/docs
•	ReDoc: http://localhost:8000/redoc



# Run tests:
pytest
pytest --cov=app
________________________________________
Coverage & Quality
•	High coverage focused on meaningful execution paths
•	No artificial coverage inflation
•	Emphasis on:
o	service logic
o	authorization boundaries
o	error handling


# Extensibility
The platform was designed with extensibility in mind. Its layered architecture (routes → services → data layer) allows new features to be introduced without structural refactoring or breaking existing functionality.
Planned and supported future enhancements include:
•	Course prerequisites
Define prerequisite courses that must be completed before a student can enroll in advanced offerings.
•	Enrollment deadlines and policies
Introduce time-based rules such as enrollment windows, withdrawal periods, and late enrollment restrictions.
•	Audit logging
Track critical system actions, including enrollments, removals, and administrative updates, to improve accountability and traceability.
•	Notification system
Integrate email or in-app notifications for enrollment confirmations, capacity limits, and administrative actions.
•	Additional user roles
Extend role-based access control to support instructors, coordinators, or academic staff with scoped permissions.
•	External frontend integration
Enable seamless integration with web or mobile frontends through the existing REST API, without backend restructuring.

# License
This project is provided for educational and academic purposes.

# Elton Ramos
# ALTSCHOOL AFRICA 
# 2026
