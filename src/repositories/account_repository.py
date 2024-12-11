from abc import ABC
from uuid import UUID

from sqlmodel import select
from typing_extensions import TypeVar

from src.models.account_model import BaseAccount
from src.repositories.base_repository import BaseRepository

T = TypeVar("T")


class BaseAccountRepository(BaseRepository[BaseAccount], ABC):
    async def get_by_user_uuid(self, user_uuid: UUID | str) -> T:
        query = select(self.model).where(self.model.user_uuid == user_uuid)
        response = await self.session.exec(query)
        return response.one_or_none()
