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


class AccountService:
    def __init__(self, session: AsyncSession):
        self.yandex_music_account_repository = YandexMusicAccountRepository(session)
        self.spotify_account_repository = SpotifyAccountRepository(session)
        self.vk_music_account_repository = VkMusicAccountRepository(session)

    async def _update_account(
        self,
        account_repository: BaseAccountRepository,
        user_uuid: UUID,
        obj: AccountBodySchema,
        out_model: type[BaseAccount],
    ):
        account = await account_repository.get_by_user_uuid(user_uuid)
        if account:
            await account_repository.delete(account)
        return await account_repository.add(out_model(**obj.model_dump(), user_uuid=user_uuid))

    async def update_yandex_music_account(
        self, user_uuid: UUID, obj: YandexMusicAccountBodySchema
    ) -> YandexMusicAccount:
        return await self._update_account(self.yandex_music_account_repository, user_uuid, obj, YandexMusicAccount)

    async def update_spotify_account(self, user_uuid: UUID, obj: SpotifyAccountBodySchema) -> SpotifyAccount:
        return await self._update_account(self.spotify_account_repository, user_uuid, obj, SpotifyAccount)

    async def update_vk_music_account(self, user_uuid: UUID, obj: VkMusicAccountBodySchema) -> VkMusicAccount:
        return await self._update_account(self.vk_music_account_repository, user_uuid, obj, VkMusicAccount)


async def get_account_service(session: AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session)
