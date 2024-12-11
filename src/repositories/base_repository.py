from abc import ABC
from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    model: type[T]

    async def get(self, session: AsyncSession, uuid: UUID | str) -> T | None:
        query = select(self.model).where(self.model.uuid == uuid)
        response = await session.exec(query)
        return response.one_or_none()

    async def get_all(self, session: AsyncSession) -> list[T]:
        query = select(self.model)
        response = await session.exec(query)
        return response.all()

    async def add(self, session: AsyncSession, obj: T) -> T:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: T) -> None:
        await session.delete(obj)
        await session.commit()
