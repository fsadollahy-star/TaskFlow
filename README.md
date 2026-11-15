# TaskFlow API

A lightweight RESTful Task Management API built with **Python, FastAPI, SQLAlchemy, and SQLite**.

TaskFlow provides a simple and well-structured backend service for managing tasks through HTTP requests and JSON responses.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update existing tasks using PATCH
- Delete tasks
- Validate input data with Pydantic
- Store task data using SQLite and SQLAlchemy
- Handle missing tasks with HTTP 404 responses
- Interactive API documentation with Swagger UI
- Automated tests with Pytest

## Technology Stack

| Technology  | Purpose              |
| ----------- | -------------------- |
| Python 3.14 | Programming language |
| FastAPI     | REST API framework   |
| SQLAlchemy  | Database ORM         |
| SQLite      | Database             |
| Pydantic    | Data validation      |
| Pytest      | Automated testing    |
| HTTPX       | API testing support  |

## Project Structure

```text
TaskFlow/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_tasks.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/fsadollahy-star/TaskFlow.git
cd TaskFlow
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the API

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Interactive Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation (ReDoc):

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

| Method | Endpoint           | Description           |
| ------ | ------------------ | --------------------- |
| GET    | `/`                | API welcome message   |
| GET    | `/health`          | Health check          |
| POST   | `/tasks`           | Create a task         |
| GET    | `/tasks`           | Retrieve all tasks    |
| GET    | `/tasks/{task_id}` | Retrieve a task by ID |
| PATCH  | `/tasks/{task_id}` | Update a task         |
| DELETE | `/tasks/{task_id}` | Delete a task         |

## Request Examples

### Create a Task

**POST** `/tasks`

Request body:

```json
{
  "title": "Learn Python REST API",
  "description": "Build the TaskFlow project",
  "completed": false,
  "priority": "high"
}
```

Successful response: `201 Created`

```json
{
  "id": 1,
  "title": "Learn Python REST API",
  "description": "Build the TaskFlow project",
  "completed": false,
  "priority": "high"
}
```

### Update a Task

**PATCH** `/tasks/1`

Request body:

```json
{
  "completed": true
}
```

### Retrieve All Tasks

**GET** `/tasks`

Returns a JSON array of tasks, ordered from newest to oldest.

### Delete a Task

**DELETE** `/tasks/1`

Successful response:

```json
{
  "message": "Task deleted successfully"
}
```

## Data Validation

TaskFlow uses Pydantic schemas to validate incoming requests.

| Field       | Validation                               |
| ----------- | ---------------------------------------- |
| title       | Required, 3–150 characters               |
| description | Optional, maximum 500 characters         |
| completed   | Boolean, defaults to false               |
| priority    | low, medium, or high; defaults to medium |

Requests containing invalid data are rejected with an HTTP 422 response.

Requests for tasks that do not exist return HTTP 404.

## Database

TaskFlow uses SQLite with SQLAlchemy ORM.

The database tables are created automatically when the application starts. The local database file is excluded from version control.

The automated test suite uses a separate temporary database.

## Running Tests

Execute the test suite:

```bash
python -m pytest -v
```

The project currently includes six automated tests covering:

- Home endpoint
- Health check
- Task creation
- Task retrieval
- Task update
- Task deletion

Latest test result:

```text
6 passed
```

## Project Status

Core CRUD operations, database integration, request validation, API documentation, and automated tests have been implemented.

This is an initial demonstration project. Authentication, user management, database migrations, and production deployment are not included in the current version.

## Author

Developed as a Python REST API portfolio project.
