from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models import SpotifyAccount, VkMusicAccount, YandexMusicAccount
from src.repositories.spotify_account_repository import SpotifyAccountRepository
from src.repositories.vk_music_account_repository import VkMusicAccountRepository
from src.repositories.yandex_music_account_repository import YandexMusicAccountRepository
from src.schemas.account_schemas import SpotifyAccountBodySchema, VkMusicAccountBodySchema, YandexMusicAccountBodySchema


class AccountService:
    def __init__(self, session: AsyncSession):
        self.yandex_music_account_repository = YandexMusicAccountRepository(session)
        self.spotify_account_repository = SpotifyAccountRepository(session)
        self.vk_music_account_repository = VkMusicAccountRepository(session)

    # TODO: MORE AND MORE ABSTRACT LAYERS FOR ACCOUNTS, NOW IT IS COOKED 💀💀💀💀
    async def _update_account(self, account_repository, user_uuid: UUID, obj):
        account = await account_repository.get_by_user_uuid(user_uuid)
        if account:
            await account_repository.delete(account)
        return await account_repository.add(YandexMusicAccount(**obj.model_dump(), user_uuid=user_uuid))

    async def update_yandex_music_account(
        self, user_uuid: UUID, obj: YandexMusicAccountBodySchema
    ) -> YandexMusicAccount:
        return await self._update_account(self.yandex_music_account_repository, user_uuid, obj)

    async def update_spotify_account(self, user_uuid: UUID, obj: SpotifyAccountBodySchema) -> SpotifyAccount:
        return await self._update_account(self.spotify_account_repository, user_uuid, obj)

    async def update_vk_music_account(self, user_uuid: UUID, obj: VkMusicAccountBodySchema) -> VkMusicAccount:
        return await self._update_account(self.vk_music_account_repository, user_uuid, obj)


async def get_account_service(session: AsyncSession = Depends(get_async_session)) -> AccountService:
    return AccountService(session)
