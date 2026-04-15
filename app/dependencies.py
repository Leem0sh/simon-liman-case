import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.db.repositories.task_repository import TaskRepository
from app.db.repositories.user_repository import UserRepository

_STUB_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:

        try:
            yield session
        finally:
            await session.close()


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(session)


def get_current_user_id(
    x_user_id: uuid.UUID | None = Header(default=None),
) -> uuid.UUID:
    return x_user_id if x_user_id is not None else _STUB_USER_ID
