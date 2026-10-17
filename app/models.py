from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    workspaces: Mapped[list["WorkspacesTable"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["TasksTable"]] = relationship(back_populates="assignee")


class WorkspacesTable(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[date] = mapped_column(Date(), default=date.today)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["UsersTable"] = relationship(back_populates="workspaces")
    tasks: Mapped[list["TasksTable"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )


class TasksTable(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="todo")
    created_at: Mapped[date] = mapped_column(Date(), default=date.today)

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    workspace: Mapped["WorkspacesTable"] = relationship(back_populates="tasks")
    assignee: Mapped["UsersTable"] = relationship(back_populates="tasks")
