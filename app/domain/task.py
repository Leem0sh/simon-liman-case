from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from app.domain.user import User


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass(frozen=True)
class Task:
    id: UUID
    title: str
    status: TaskStatus
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    assignee_id: UUID | None = None

    def can_be_edited_by(self, user: User) -> bool:
        return user.is_active and user.id == self.owner_id

    def complete(self) -> "Task":
        if self.status is not TaskStatus.IN_PROGRESS:
            raise ValueError(
                f"Cannot complete task in status '{self.status}'. "
                "Task must be IN_PROGRESS to be completed."
            )
        return replace(self, status=TaskStatus.DONE)

    def assign_to(self, user: User) -> "Task":
        if not user.is_active:
            raise ValueError("Cannot assign task to an inactive user.")
        if self.status is TaskStatus.DONE:
            raise ValueError("Cannot reassign a task that is already DONE.")
        return replace(self, assignee_id=user.id)
