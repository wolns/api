from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models.account_model import BaseAccount
from src.models.track_model import Track
from src.services.account_service import AccountService
from src.services.music_service import MusicService
from src.services.music_services.spotify_service import SpotifyService
from src.services.music_services.yandex_music_service import YandexMusicService
from src.services.track_service import TrackService


class TrackUpdateService:
    def __init__(
        self, track_service: TrackService, account_service: AccountService, music_services: list[MusicService]
    ) -> None:
        self.track_service = track_service
        self.account_service = account_service
        self.music_services = {service.service_type: service for service in music_services}

    async def update_tracks(self):
        update_tracks = await self.track_service.get_update_tracks()
        for update_track in update_tracks:
            await self.update_user_track(update_track.user_uuid, update_track)

    async def update_user_track(self, user_uuid: UUID, track: Track | None = None):
        accounts = [
            await self.account_service.get_yandex_music_account(user_uuid),
            await self.account_service.get_spotify_account(user_uuid),
            await self.account_service.get_vk_music_account(user_uuid),
        ]
        for account in accounts:
            if account and account.service_type in self.music_services:
                music_service = self.music_services[account.service_type]
                if await self.update_user_track_with_service(account, music_service, track):
                    break

    async def update_user_track_with_service(
        self, account: BaseAccount, music_service: MusicService, track: Track | None = None
    ) -> Track | None:
        if not track:
            track = await self.track_service.get_track_by_user_uuid(account.user_uuid)
        current_track = await music_service.get_current_track(account)
        if current_track:
            if not track:
                track = Track(user_uuid=account.user_uuid)
            track.title = current_track.title
            track.artists = current_track.artists
            track.cover = current_track.cover
            track.service_type = music_service.service_type
            return await self.track_service.update_track(track)
        return None


async def get_track_update_service(session: AsyncSession = Depends(get_async_session)) -> TrackUpdateService:
    track_service = TrackService(session)
    account_service = AccountService(session)
    music_services = [
        YandexMusicService(),
        SpotifyService(),
    ]
    return TrackUpdateService(track_service, account_service, music_services)
