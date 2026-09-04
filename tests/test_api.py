import pytest
from app import create_app
import app.routes as routes


@pytest.fixture()
def client():
    routes.tasks.clear()
    routes.next_task_id = 1

    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client

    routes.tasks.clear()
    routes.next_task_id = 1


def test_home_returns_application_info(client):
    response = client.get("/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "DevOps Task Manager"
    assert data["message"] == "Task Manager API is running"


def test_health_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_task(client):
    response = client.post("/tasks", json={
        "title": "Learn Docker",
        "description": "Understand containers",
        "priority": "high"
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["title"] == "Learn Docker"
    assert data["completed"] is False


def test_create_task_rejects_invalid_priority(client):
    response = client.post("/tasks", json={
        "title": "Learn Kubernetes",
        "priority": "urgent"
    })

    assert response.status_code == 400
    assert "priority" in response.get_json()["error"]


def test_get_missing_task_returns_404(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "task not found"


def test_update_task(client):
    create_response = client.post("/tasks", json={
        "title": "Learn Docker"
    })
    task_id = create_response.get_json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "completed": True,
        "priority": "medium"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["completed"] is True
    assert data["priority"] == "medium"


def test_delete_task(client):
    create_response = client.post("/tasks", json={
        "title": "Temporary task"
    })
    task_id = create_response.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404
