from uuid import UUID

from sqlmodel import select
from typing_extensions import TypeVar

from src.models.track_model import Track
from src.repositories.base_repository import BaseRepository

T = TypeVar("T")


class TrackRepository(BaseRepository[Track]):
    model = Track

    async def get_by_user_uuid(self, user_uuid: UUID | str) -> T | None:
        query = select(self.model).where(self.model.user_uuid == user_uuid)
        response = await self.session.exec(query)
        return response.one_or_none()
