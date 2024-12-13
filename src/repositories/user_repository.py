from datetime import datetime, timedelta

from sqlmodel import select

from src.core.timezone import tz
from src.models import User
from src.models.track_model import Track
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_login(self, login: str) -> User:
        query = select(self.model).where(self.model.login == login)
        response = await self.session.exec(query)
        return response.one_or_none()

    async def get_without_track(self) -> list[User]:
        query = select(self.model).where(self.model.track == None)
        response = await self.session.exec(query)
        return response.all()

    async def get_with_old_tracks(self, minutes: int = 1) -> list[User]:
        threshold_time = datetime.now(tz) - timedelta(minutes=minutes)
        query = select(User).join(Track).where(Track.updated_at < threshold_time)
        response = await self.session.exec(query)
        return response.all()
