---
name: task-management-api
description: Use when working in this repo's Task Management REST API codebase (app/ or tests/) — adding fields, endpoints, or tests to the FastAPI Task model, in-memory repository, or routes. Covers project structure, conventions, and how to run/verify changes.
---

# Task Management API Codebase

FastAPI-based in-memory Task Management REST API.

## Structure

```
app/
  models.py      # Pydantic models: Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority enums
  repository.py  # TaskRepository: in-memory CRUD + filtering; module-level `task_repository` singleton
  routes.py      # APIRouter with /tasks endpoints; translates TaskNotFoundError -> HTTPException
  main.py        # FastAPI app, RequestValidationError -> 400 handler, uvicorn entry point
tests/
  conftest.py    # `client` fixture (TestClient) + autouse `reset_repository` fixture
  test_tasks.py  # grouped into TestCreateTask / TestGetTasks / TestUpdateTask / TestDeleteTask
```

## Conventions

- **Adding a Task field**: update all three schemas in `models.py` (`Task`, `TaskCreate`, `TaskUpdate`) as `Optional[...] = None` (or with a default) for backward compatibility. Then wire it into `TaskRepository.create_task` explicitly (it builds the `Task` field-by-field, it does NOT unpack `task_data`). `update_task` needs no change per-field — it merges via `task_data.model_dump(exclude_unset=True)` automatically, which also supports clearing a field by sending it as `null`.
- **Filtering** (`get_all_tasks`): add an `Optional[...] = None` parameter and filter with a list comprehension only when the value is not `None`. Wire the same param through `routes.py`'s `GET /tasks` as a `Query(default=None)`.
- **Error handling**: repository methods raise `TaskNotFoundError` for missing ids; routes catch it and raise `HTTPException(404)`. Invalid request bodies are handled globally — `main.py` converts FastAPI's default 422 (`RequestValidationError`) into 400 to match this API's contract. `PUT` with an empty body returns 400 explicitly in the route handler.
- **Tests**: every new field/endpoint needs (a) a fixture default in `_create_task()`'s payload, (b) a creation test, (c) an update/reassign test, (d) a filter test if filterable, (e) a 404/400 edge case if applicable.

## Verify changes

```bash
source .venv/bin/activate
pytest -q
```

Run the server for manual checks: `uvicorn app.main:app --reload` (docs at `/docs`).
