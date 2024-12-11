from src.models import YandexMusicAccount
from src.repositories.base_repository import BaseRepository


class YandexMusicAccountRepository(BaseRepository[YandexMusicAccount]):
    model = YandexMusicAccount
