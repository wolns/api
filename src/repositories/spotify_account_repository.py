from src.models import SpotifyAccount
from src.repositories.account_repository import BaseAccountRepository


class SpotifyAccountRepository(BaseAccountRepository):
    model = SpotifyAccount
