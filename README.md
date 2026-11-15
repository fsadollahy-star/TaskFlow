
# TaskFlow API

A RESTful Task Management API built with Python, FastAPI, and SQLite.

## Overview

TaskFlow is a lightweight REST API that allows users to create, retrieve, update, and delete tasks.

The project demonstrates REST API development, database integration, request validation, and automated testing.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update existing tasks
- Delete tasks
- Input validation using Pydantic
- SQLite database integration
- Interactive API documentation with Swagger UI
- Automated tests using Pytest

## Technology Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- HTTPX

## Project Structure

    TaskFlow/
    ├── app/
    │   ├── __init__.py
    │   └── main.py
    ├── tests/
    │   └── test_tasks.py
    ├── taskflow.db
    ├── requirements.txt
    └── README.md

## Installation

### 1. Clone the repository

    git clone YOUR_REPOSITORY_URL
    cd TaskFlow

### 2. Create a virtual environment

    python -m venv .venv

### 3. Activate the environment

Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 4. Install dependencies

    pip install -r requirements.txt

## Run the API

    python -m uvicorn app.main:app --reload

The API will be available at:

    http://127.0.0.1:8000

## API Documentation

Swagger UI:

    http://127.0.0.1:8000/docs

Alternative documentation:

    http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API welcome message |
| GET | /health | Health check |
| POST | /tasks | Create a task |
| GET | /tasks | Retrieve all tasks |
| GET | /tasks/{task_id} | Retrieve a task |
| PATCH | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Example Request

Create a task:

    POST /tasks

Request body:

    {
        "title": "Learn Python REST API",
        "description": "Build TaskFlow project",
        "completed": false,
        "priority": "high"
    }

## Run Automated Tests

    python -m pytest -v

The project includes automated tests for:

- Home endpoint
- Health check
- Task creation
- Task retrieval
- Task update
- Task deletion

## Database

TaskFlow uses SQLite and SQLAlchemy for database operations.

The test suite uses a separate temporary SQLite database to avoid modifying the main application database.

## Project Status

Core CRUD functionality and automated tests are implemented.

This project is an initial demonstration version. Authentication, user management, database migrations, and production deployment are not yet implemented.

## License

MIT License
