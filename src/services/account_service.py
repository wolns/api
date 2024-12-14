from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models import SpotifyAccount, VkMusicAccount, YandexMusicAccount
from src.models.account_model import BaseAccount
from src.repositories.account_repository import BaseAccountRepository
from src.repositories.spotify_account_repository import SpotifyAccountRepository
from src.repositories.vk_music_account_repository import VkMusicAccountRepository
from src.repositories.yandex_music_account_repository import YandexMusicAccountRepository
from src.schemas.account_schemas import (
    AccountBodySchema,
    SpotifyAccountBodySchema,
    VkMusicAccountBodySchema,
    YandexMusicAccountBodySchema,
)
from src.services.music_services.spotify_service import SpotifyService
from src.services.music_services.yandex_music_service import YandexMusicService


class AccountService:
    def __init__(self, session: AsyncSession):
        self.yandex_music_account_repository = YandexMusicAccountRepository(session)
        self.spotify_account_repository = SpotifyAccountRepository(session)
        self.vk_music_account_repository = VkMusicAccountRepository(session)
        music_services = [
            YandexMusicService(),
            SpotifyService(),
        ]
        self.music_services = {service.service_type: service for service in music_services}

    async def _update_account(
        self,
        account_repository: BaseAccountRepository,
        user_uuid: UUID,
        obj: AccountBodySchema,
    ):
        account = await account_repository.get_by_user_uuid(user_uuid)
        if account:
            await account_repository.delete(account)
        return await account_repository.add(account_repository.model(**obj.model_dump(), user_uuid=user_uuid))

    async def update_yandex_music_account(
        self, user_uuid: UUID, obj: YandexMusicAccountBodySchema
    ) -> YandexMusicAccount:
        return await self._update_account(self.yandex_music_account_repository, user_uuid, obj)

    async def update_spotify_account(self, user_uuid: UUID, obj: SpotifyAccountBodySchema) -> SpotifyAccount:
        return await self._update_account(self.spotify_account_repository, user_uuid, obj)

    async def update_vk_music_account(self, user_uuid: UUID, obj: VkMusicAccountBodySchema) -> VkMusicAccount:
        return await self._update_account(self.vk_music_account_repository, user_uuid, obj)

    async def _get_account(
        self,
        account_repository: BaseAccountRepository,
        user_uuid: UUID,
    ) -> BaseAccount | None:
        return await account_repository.get_by_user_uuid(user_uuid)

    async def get_yandex_music_account(self, user_uuid: UUID) -> YandexMusicAccount | None:
        return await self._get_account(self.yandex_music_account_repository, user_uuid)

    async def get_spotify_account(self, user_uuid: UUID) -> SpotifyAccount | None:
        return await self._get_account(self.spotify_account_repository, user_uuid)

    async def get_vk_music_account(self, user_uuid: UUID) -> VkMusicAccount | None:
        return await self._get_account(self.vk_music_account_repository, user_uuid)

    async def _refresh_account(
        self,
        account_repository: BaseAccountRepository,
        user_uuid: UUID,
        refresh_token: str,
    ):
        new_tokens = await self.music_services[account_repository.model.service_type].refresh_tokens(refresh_token)
        return await self._update_account(account_repository, user_uuid, new_tokens)

    async def refresh_yandex_music_account(self, user_uuid: UUID, refresh_token: str) -> YandexMusicAccount:
        return await self._refresh_account(self.yandex_music_account_repository, user_uuid, refresh_token)

    async def refresh_spotify_account(self, user_uuid: UUID, refresh_token: str) -> SpotifyAccount:
        return await self._refresh_account(self.spotify_account_repository, user_uuid, refresh_token)


async def get_account_service(session: AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session)
