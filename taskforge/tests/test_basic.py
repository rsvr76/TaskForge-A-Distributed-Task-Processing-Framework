import pytest
import time
from fastapi.testclient import TestClient
from taskforge.app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TaskForge running"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "queue_size" in data
    assert "tasks_in_registry" in data


def test_create_task():
    response = client.post("/api/tasks", json={
        "task_type": "sleep",
        "payload": {"seconds": 1}
    })
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "PENDING"


def test_create_task_invalid_type():
    response = client.post("/api/tasks", json={
        "task_type": "invalid",
        "payload": {}
    })
    assert response.status_code == 400
    assert "Unknown task type" in response.json()["detail"]


def test_get_task_status():
    response = client.post("/api/tasks", json={
        "task_type": "sleep",
        "payload": {"seconds": 1}
    })
    task_id = response.json()["task_id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "PENDING"


def test_get_nonexistent_task():
    response = client.get("/api/tasks/nonexistent")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


def test_get_task_result_before_completion():
    response = client.post("/api/tasks", json={
        "task_type": "sleep",
        "payload": {"seconds": 1}
    })
    task_id = response.json()["task_id"]

    response = client.get(f"/api/tasks/{task_id}/result")
    assert response.status_code == 400
    assert "not completed" in response.json()["detail"]


def test_concurrent_task_creation():
    import threading

    results = []

    def create_task():
        response = client.post("/api/tasks", json={
            "task_type": "sleep",
            "payload": {"seconds": 1}
        })
        results.append(response.json())

    threads = []
    for _ in range(5):
        t = threading.Thread(target=create_task)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    assert len(results) == 5
    for result in results:
        assert "task_id" in result
        assert result["status"] == "PENDING"
