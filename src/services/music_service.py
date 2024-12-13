from abc import ABC, abstractmethod

from src.schemas.account_schemas import AccountBodySchema
from src.schemas.track_schemas import TrackBaseInfo


class MusicService(ABC):
    @abstractmethod
    async def get_current_track(self, obj: AccountBodySchema) -> TrackBaseInfo | None:
        pass
