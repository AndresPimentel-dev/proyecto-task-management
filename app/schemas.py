from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(description="name", min_length=1, max_length=50)
    email: EmailStr = Field(description="email", min_length=1, max_length=50)
    password: str = Field(description="password", min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "John Doe",
                "email": "jhondoe@gmail.com",
                "password": "123456",
            }
        }
    }


class WorkspaceCreate(BaseModel):
    name: str = Field(description="workspace name", min_length=1, max_length=50)
    description: str = Field(
        description="workspace description", min_length=1, max_length=255
    )
    created_at: date | None = Field(
        default=None, description="workspace's creation date (optional)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {"name": "My Workspace", "description": "This is my workspace"}
        }
    }


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(
        default=None, description="workspace name", min_length=1, max_length=50
    )
    description: str | None = Field(
        default=None, description="workspace description", min_length=1, max_length=255
    )


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    title: str = Field(description="task title", min_length=1, max_length=50)
    description: str = Field(
        description="task description", min_length=1, max_length=255
    )
    status: TaskStatus = Field(default=TaskStatus.TODO, description="task status")
    created_at: date | None = Field(
        default=None, description="task's creation date (optional)"
    )
    workspace_id: int = Field(description="workspace id", ge=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "learn coding",
                "description": "i have to learn CI",
                "status": "todo",
                "workspace_id": 1,
            }
        }
    }


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None, description="task title", min_length=1, max_length=50
    )
    description: str | None = Field(
        default=None, description="task description", min_length=1, max_length=255
    )
    status: TaskStatus | None = Field(default=None, description="task status")


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: date
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class WorkspacesListResponse(BaseModel):
    workspaces: list[WorkspaceResponse]

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: date
    workspace_id: int
    assignee_id: int

    model_config = ConfigDict(from_attributes=True)


class TasksListResponse(BaseModel):
    tasks: list[TaskResponse]
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str = Field(description="access token in str")
    token_type: str = Field(description="token type in str")
