from src.models import YandexMusicAccount
from src.repositories.account_repository import BaseAccountRepository


class YandexMusicAccountRepository(BaseAccountRepository):
    model = YandexMusicAccount
