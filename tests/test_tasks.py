def _create_task(client, **overrides):
    payload = {
        "title": "Write unit tests",
        "description": "Cover CRUD endpoints",
        "status": "pending",
        "priority": "high",
    }
    payload.update(overrides)
    return client.post("/tasks", json=payload)


class TestCreateTask:
    def test_create_task_success(self, client):
        response = _create_task(client)
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Write unit tests"
        assert body["status"] == "pending"
        assert body["priority"] == "high"
        assert "id" in body
        assert "created_at" in body

    def test_create_task_missing_title_returns_400(self, client):
        response = client.post("/tasks", json={"description": "no title"})
        assert response.status_code == 400

    def test_create_task_blank_title_returns_400(self, client):
        response = _create_task(client, title="")
        assert response.status_code == 400

    def test_create_task_invalid_status_returns_400(self, client):
        response = _create_task(client, status="not_a_status")
        assert response.status_code == 400

    def test_create_task_invalid_priority_returns_400(self, client):
        response = _create_task(client, priority="urgent")
        assert response.status_code == 400


class TestGetTasks:
    def test_get_all_tasks_empty(self, client):
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_tasks_returns_created_tasks(self, client):
        _create_task(client, title="Task 1")
        _create_task(client, title="Task 2")
        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_all_tasks_filter_by_status(self, client):
        _create_task(client, title="Pending task", status="pending")
        _create_task(client, title="Done task", status="completed")
        response = client.get("/tasks", params={"status": "completed"})
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["title"] == "Done task"

    def test_get_task_by_id_success(self, client):
        created = _create_task(client).json()
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_get_task_by_id_not_found_returns_404(self, client):
        response = client.get("/tasks/9999")
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_success(self, client):
        created = _create_task(client).json()
        response = client.put(
            f"/tasks/{created['id']}",
            json={"status": "in_progress", "title": "Updated title"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "in_progress"
        assert body["title"] == "Updated title"
        assert body["description"] == created["description"]

    def test_update_task_not_found_returns_404(self, client):
        response = client.put("/tasks/9999", json={"title": "Nope"})
        assert response.status_code == 404

    def test_update_task_empty_body_returns_400(self, client):
        created = _create_task(client).json()
        response = client.put(f"/tasks/{created['id']}", json={})
        assert response.status_code == 400

    def test_update_task_invalid_status_returns_400(self, client):
        created = _create_task(client).json()
        response = client.put(f"/tasks/{created['id']}", json={"status": "bogus"})
        assert response.status_code == 400


class TestDeleteTask:
    def test_delete_task_success(self, client):
        created = _create_task(client).json()
        response = client.delete(f"/tasks/{created['id']}")
        assert response.status_code == 204

        get_response = client.get(f"/tasks/{created['id']}")
        assert get_response.status_code == 404

    def test_delete_task_not_found_returns_404(self, client):
        response = client.delete("/tasks/9999")
        assert response.status_code == 404


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
