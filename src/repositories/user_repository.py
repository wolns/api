from abc import ABC, abstractmethod

from src.models import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    async def get_by_login(self, login: str) -> User:
        pass
