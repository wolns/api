from datetime import datetime, timedelta
from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.timezone import tz
from src.database.database import get_async_session
from src.models.track_model import Track
from src.repositories.track_repository import TrackRepository
from src.schemas.track_schemas import TrackGetResponseSchema


class TrackService:
    def __init__(self, session: AsyncSession):
        self.track_repository = TrackRepository(session)

    async def get_track_by_user_uuid(self, user_uuid: UUID) -> Track | None:
        return await self.track_repository.get_by_user_uuid(user_uuid)

    async def get_recently_updated_track_by_user_uuid(self, user_uuid: UUID) -> Track | None:
        return await self.track_repository.get_recently_updated_by_user_uuid(user_uuid)

    async def get_update_tracks(self) -> list[Track]:
        return await self.track_repository.get_update_tracks()

    async def to_response_model(self, track: Track) -> TrackGetResponseSchema:
        threshold_time = datetime.now(tz) - timedelta(minutes=1)
        is_playing = track.updated_at > threshold_time
        return TrackGetResponseSchema(
            user_name=track.user.name,
            is_playing=is_playing,
            service_type=track.service_type,
            title=track.title,
            artists=track.artists,
            cover=track.cover,
        )


async def get_track_service(session: AsyncSession = Depends(get_async_session)) -> TrackService:
    return TrackService(session)
