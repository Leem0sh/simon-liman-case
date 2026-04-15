from uuid import UUID

from sqlalchemy import select

from app.db.models.task import TaskModel
from app.db.repositories.base import BaseRepository
from app.domain.task import Task, TaskStatus


class TaskRepository(BaseRepository[TaskModel, Task]):
    model_class = TaskModel

    def _to_domain(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            owner_id=model.owner_id,
            assignee_id=model.assignee_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, domain: Task) -> TaskModel:
        return TaskModel(
            id=domain.id,
            title=domain.title,
            description=domain.description,
            status=domain.status,
            owner_id=domain.owner_id,
            assignee_id=domain.assignee_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    async def get_by_owner(self, owner_id: UUID) -> list[Task]:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.owner_id == owner_id)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_by_assignee(self, assignee_id: UUID) -> list[Task]:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.assignee_id == assignee_id)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_by_status(self, status: TaskStatus) -> list[Task]:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.status == status)
        )
        return [self._to_domain(m) for m in result.scalars().all()]
