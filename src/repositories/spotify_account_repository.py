from abc import ABC

from src.models import SpotifyAccount
from src.repositories.base_repository import BaseRepository


class SpotifyAccountRepository(BaseRepository[SpotifyAccount], ABC):
    pass
