import uuid
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.db.repositories.task_repository import TaskRepository
from app.db.repositories.user_repository import UserRepository
from app.domain.task import Task, TaskStatus
from app.schemas.task import TaskCreate


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        user_repository: UserRepository,
    ) -> None:
        self._tasks = task_repository
        self._users = user_repository

    async def create_task(self, data: TaskCreate, owner_id: UUID) -> Task:
        owner = await self._users.get_by_id(owner_id)
        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{owner_id}' not found.",
            )

        now = datetime.now(tz=timezone.utc)
        task = Task(
            id=uuid.uuid4(),
            title=data.title,
            description=data.description,
            status=TaskStatus.TODO,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
        )

        if data.assignee_id is not None:
            assignee = await self._users.get_by_id(data.assignee_id)
            if assignee is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Assignee '{data.assignee_id}' not found.",
                )
            try:
                task = task.assign_to(assignee)
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=str(exc),
                ) from exc

        return await self._tasks.save(task)

    async def get_task(self, task_id: UUID) -> Task:
        task = await self._tasks.get_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task '{task_id}' not found.",
            )
        return task
