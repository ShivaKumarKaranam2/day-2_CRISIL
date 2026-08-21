# day-2_CRISIL

## Task Management REST API

A simple in-memory Task Management REST API built with FastAPI.

### Project Structure

```
app/
  __init__.py
  models.py      # Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority enums
  repository.py  # In-memory TaskRepository (create/get/update/delete + status filter)
  routes.py      # /tasks endpoints with 404/400 error handling
  main.py        # FastAPI app, validation error handler, entry point
tests/
  conftest.py    # TestClient fixture + repository reset between tests
  test_tasks.py  # CRUD tests and edge cases (missing/blank title, invalid enums, 404s)
requirements.txt
pytest.ini
```

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Run tests

```bash
pytest -q
```

### API Endpoints

| Method | Path              | Description                                  |
|--------|-------------------|-----------------------------------------------|
| POST   | `/tasks`          | Create a task                                 |
| GET    | `/tasks`          | List tasks (optional `?status=` filter)       |
| GET    | `/tasks/{id}`     | Get a task by id (404 if not found)           |
| PUT    | `/tasks/{id}`     | Update a task (400 if body is empty/invalid)  |
| DELETE | `/tasks/{id}`     | Delete a task (404 if not found)              |
| GET    | `/health`         | Health check                                  |

### Task Fields

- `id`: integer, auto-generated
- `title`: string, required
- `description`: string, optional
- `status`: `pending` | `in_progress` | `completed`
- `priority`: `low` | `medium` | `high`
- `created_at`: timestamp, auto-generated