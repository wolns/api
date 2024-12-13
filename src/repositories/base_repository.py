from abc import ABC
from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, uuid: UUID | str) -> T | None:
        query = select(self.model).where(self.model.uuid == uuid)
        response = await self.session.exec(query)
        return response.one_or_none()

    async def get_all(self) -> list[T]:
        query = select(self.model)
        response = await self.session.exec(query)
        return response.all()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def update(self, obj: T) -> T:
        if await self.get(obj.uuid):
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        return await self.add(obj)
