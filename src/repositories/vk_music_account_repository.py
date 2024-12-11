from abc import ABC

from src.models import VkMusicAccount
from src.repositories.base_repository import BaseRepository


class VkMusicAccountRepository(BaseRepository[VkMusicAccount], ABC):
    pass
