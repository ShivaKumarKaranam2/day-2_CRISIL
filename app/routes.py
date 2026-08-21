from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate
from app.repository import TaskNotFoundError, task_repository

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate) -> Task:
    return task_repository.create_task(task_data)


@router.get("", response_model=list[Task])
def get_all_tasks(status_filter: Optional[TaskStatus] = Query(default=None, alias="status")) -> list[Task]:
    return task_repository.get_all_tasks(status=status_filter)


@router.get("/{task_id}", response_model=Task)
def get_task_by_id(task_id: int) -> Task:
    try:
        return task_repository.get_task_by_id(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate) -> Task:
    if not task_data.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided to update a task",
        )
    try:
        return task_repository.update_task(task_id, task_data)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    try:
        task_repository.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
