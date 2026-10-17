from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.limiter import limiter
from app.models import UsersTable, WorkspacesTable
from app.schemas import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspacesListResponse,
    WorkspaceUpdate,
)

router = APIRouter(prefix="/api/v1.0", tags=["Workspaces"])


# ==========================================
#       CRUD DE WORKSPACES (PROTEGIDO)
# ==========================================


@router.post(
    "/workspaces",
    status_code=status.HTTP_201_CREATED,
    response_model=WorkspaceResponse,
)
@limiter.limit("60/minute")
def create_workspace(
    request: Request,
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    creation_date = workspace_data.created_at or date.today()
    new_workspace = WorkspacesTable(
        name=workspace_data.name,
        description=workspace_data.description,
        owner_id=current_user.id,
        created_at=creation_date,
    )
    try:
        db.add(new_workspace)
        db.commit()
        db.refresh(new_workspace)
        return new_workspace
    except Exception:
        db.rollback()
        raise


@router.get(
    "/workspaces",
    status_code=status.HTTP_200_OK,
    response_model=WorkspacesListResponse,
)
@limiter.limit("60/minute")
def list_workspaces(
    request: Request,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    workspaces = (
        db.query(WorkspacesTable)
        .filter(WorkspacesTable.owner_id == current_user.id)
        .all()
    )
    return {"workspaces": workspaces}


@router.get(
    "/workspaces/{workspace_id}",
    status_code=status.HTTP_200_OK,
    response_model=WorkspaceResponse,
)
@limiter.limit("60/minute")
def read_workspace(
    request: Request,
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    workspace = (
        db.query(WorkspacesTable)
        .filter(
            WorkspacesTable.id == workspace_id,
            WorkspacesTable.owner_id == current_user.id,
        )
        .first()
    )
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or unauthorized",
        )
    return workspace


@router.put(
    "/workspaces/{workspace_id}",
    status_code=status.HTTP_200_OK,
    response_model=WorkspaceResponse,
)
@limiter.limit("60/minute")
def update_workspace(
    request: Request,
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    workspace = (
        db.query(WorkspacesTable)
        .filter(
            WorkspacesTable.id == workspace_id,
            WorkspacesTable.owner_id == current_user.id,
        )
        .first()
    )
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or unauthorized",
        )

    if workspace_data.name is not None:
        workspace.name = workspace_data.name
    if workspace_data.description is not None:
        workspace.description = workspace_data.description

    try:
        db.commit()
        db.refresh(workspace)
        return workspace
    except Exception:
        db.rollback()
        raise


@router.delete("/workspaces/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
def delete_workspace(
    request: Request,
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: UsersTable = Depends(get_current_user),
):
    workspace = (
        db.query(WorkspacesTable)
        .filter(
            WorkspacesTable.id == workspace_id,
            WorkspacesTable.owner_id == current_user.id,
        )
        .first()
    )
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or unauthorized",
        )

    try:
        db.delete(workspace)
        db.commit()
    except Exception:
        db.rollback()
        raise
