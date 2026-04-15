from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.repositories.task_repository import TaskRepository
from app.db.repositories.user_repository import UserRepository
from app.dependencies import (
    get_current_user_id,
    get_task_repository,
    get_user_repository,
)
from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import TaskService

router = APIRouter()


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> TaskService:
    return TaskService(task_repo, user_repo)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    owner_id: UUID = Depends(get_current_user_id),
) -> TaskRead:
    task = await service.create_task(data=data, owner_id=owner_id)
    return TaskRead.model_validate(task)
