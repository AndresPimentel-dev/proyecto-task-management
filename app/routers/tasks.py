from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.limiter import limiter
from app.models import TasksTable, UsersTable, WorkspacesTable
from app.schemas import (
    TaskCreate,
    TaskResponse,
    TasksListResponse,
    TaskStatus,
    TaskUpdate,
)

router = APIRouter(prefix="/api/v1.0", tags=["Tasks"])


# ==========================================
#          CRUD DE TAREAS (PROTEGIDO)
# ==========================================


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse,
)
@limiter.limit("60/minute")
def create_task(
    request: Request,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    workspace = (
        db.query(WorkspacesTable)
        .filter(
            WorkspacesTable.id == task_data.workspace_id,
            WorkspacesTable.owner_id == current_user.id,
        )
        .first()
    )
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace no encontrado o no autorizado",
        )

    task_status = (
        task_data.status.value
        if hasattr(task_data.status, "value")
        else (task_data.status or "todo")
    )
    creation_date = task_data.created_at or date.today()

    new_task = TasksTable(
        title=task_data.title,
        description=task_data.description,
        status=task_status,
        created_at=creation_date,
        workspace_id=workspace.id,
        assignee_id=current_user.id,
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception:
        db.rollback()
        raise


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TasksListResponse,
)
@limiter.limit("60/minute")
def read_tasks(
    request: Request,
    workspace_id: int | None = Query(default=None, description="Filtrar por workspace"),
    task_status: TaskStatus | None = Query(
        default=None, alias="status", description="Filtrar por estado"
    ),
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    query = db.query(TasksTable).filter(TasksTable.assignee_id == current_user.id)

    if workspace_id is not None:
        query = query.filter(TasksTable.workspace_id == workspace_id)
    if task_status is not None:
        val = task_status.value if hasattr(task_status, "value") else task_status
        query = query.filter(TasksTable.status == val)

    tasks = query.all()
    return {"tasks": tasks}


@router.get(
    "/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponse,
)
@limiter.limit("60/minute")
def read_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    task = (
        db.query(TasksTable)
        .filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or unauthorized",
        )
    return task


@router.put(
    "/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponse,
)
@limiter.limit("60/minute")
def update_task(
    request: Request,
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    task = (
        db.query(TasksTable)
        .filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or unauthorized",
        )

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = (
            task_data.status.value
            if hasattr(task_data.status, "value")
            else task_data.status
        )

    try:
        db.commit()
        db.refresh(task)
        return task
    except Exception:
        db.rollback()
        raise


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
def delete_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    task = (
        db.query(TasksTable)
        .filter(TasksTable.id == task_id, TasksTable.assignee_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or unauthorized",
        )

    try:
        db.delete(task)
        db.commit()
    except Exception:
        db.rollback()
        raise
