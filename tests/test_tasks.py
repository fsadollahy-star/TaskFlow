import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import main


@pytest.fixture
def client(tmp_path):
    test_db = tmp_path / "test.db"

    test_engine = create_engine(
        f"sqlite:///{test_db}",
        connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    main.Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[main.get_db] = override_get_db

    with TestClient(main.app) as test_client:
        yield test_client

    main.app.dependency_overrides.clear()
    test_engine.dispose()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing API",
            "completed": False,
            "priority": "high"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


def test_read_tasks(client):
    client.post(
        "/tasks",
        json={"title": "First Task"}
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Original Task"}
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Task to Delete"}
    )

    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    check = client.get(f"/tasks/{task_id}")

    assert check.status_code == 404