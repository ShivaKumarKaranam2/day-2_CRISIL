from datetime import datetime, timezone
from itertools import count
from threading import Lock
from typing import Optional

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a task with the given id does not exist."""


class TaskRepository:
    """In-memory storage layer for Task entities."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._id_counter = count(start=1)
        self._lock = Lock()

    def create_task(self, task_data: TaskCreate) -> Task:
        with self._lock:
            task_id = next(self._id_counter)
            task = Task(
                id=task_id,
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                priority=task_data.priority,
                created_at=datetime.now(timezone.utc),
            )
            self._tasks[task_id] = task
            return task

    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
        return sorted(tasks, key=lambda task: task.id)

    def get_task_by_id(self, task_id: int) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        with self._lock:
            existing = self.get_task_by_id(task_id)
            updated = existing.model_copy(
                update=task_data.model_dump(exclude_unset=True)
            )
            self._tasks[task_id] = updated
            return updated

    def delete_task(self, task_id: int) -> None:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(f"Task with id {task_id} not found")
            del self._tasks[task_id]


# Singleton repository instance used across the app
task_repository = TaskRepository()
