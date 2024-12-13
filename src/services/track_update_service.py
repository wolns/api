from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.account_service import AccountService
from src.services.track_service import TrackService


class TrackUpdateService:
    def __init__(self, track_service: TrackService, account_service: AccountService) -> None:
        self.track_service = track_service
        self.account_service = account_service

    async def update_tracks(self):
        update_tracks = await self.track_service.get_update_tracks()

    async def update_user_track(self):
        pass


async def get_track_update_service(session: AsyncSession) -> TrackUpdateService:
    track_service = TrackService(session)
    account_service = AccountService(session)
    return TrackUpdateService(track_service, account_service)
