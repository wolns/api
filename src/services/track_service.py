from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.repositories.track_repository import TrackRepository


class TrackService:
    def __init__(self, session: AsyncSession):
        self.track_repository = TrackRepository(session)


async def get_track_service(session: AsyncSession = Depends(get_async_session)) -> TrackService:
    return TrackService(session)
