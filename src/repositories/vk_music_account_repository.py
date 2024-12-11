from src.models import VkMusicAccount
from src.repositories.account_repository import BaseAccountRepository


class VkMusicAccountRepository(BaseAccountRepository):
    model = VkMusicAccount
