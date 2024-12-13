from datetime import datetime, timedelta
from uuid import UUID

from sqlmodel import select
from typing_extensions import TypeVar

from src.core.timezone import tz
from src.models.track_model import Track
from src.repositories.base_repository import BaseRepository

T = TypeVar("T")


class TrackRepository(BaseRepository[Track]):
    model = Track

    async def get_by_user_uuid(self, user_uuid: UUID | str) -> T | None:
        query = select(Track).where(Track.user_uuid == user_uuid)
        response = await self.session.exec(query)
        return response.one_or_none()

    async def get_recently_updated_by_user_uuid(self, user_uuid: UUID, minutes: int = 1) -> T | None:
        threshold_time = datetime.now(tz) - timedelta(minutes=minutes)
        query = select(Track).where(Track.user_uuid == user_uuid, Track.updated_at > threshold_time)
        response = await self.session.exec(query)
        return response.one_or_none()

    async def get_update_tracks(self, minutes: int = 1) -> list[T]:
        threshold_time = datetime.now(tz) - timedelta(minutes=minutes)
        query = select(Track).where(Track.updated_at < threshold_time)
        response = await self.session.exec(query)
        return response.all()
