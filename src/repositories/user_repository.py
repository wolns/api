from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_login(self, session: AsyncSession, login: str) -> User:
        query = select(self.model).where(self.model.login == login)
        response = await session.exec(query)
        return response
