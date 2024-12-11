from uuid import UUID

from sqlmodel import select

from src.models import SpotifyAccount
from src.repositories.base_repository import BaseRepository


class SpotifyAccountRepository(BaseRepository[SpotifyAccount]):
    model = SpotifyAccount

    async def get_by_user_uuid(self, user_uuid: UUID | str) -> SpotifyAccount:
        query = select(self.model).where(self.model.user_uuid == user_uuid)
        response = await self.session.exec(query)
        return response.one_or_none()
