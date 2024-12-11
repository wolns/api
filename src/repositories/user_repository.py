from sqlmodel import select

from src.models import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_login(self, login: str) -> User:
        query = select(self.model).where(self.model.login == login)
        response = await self.session.exec(query)
        return response.one_or_none()
