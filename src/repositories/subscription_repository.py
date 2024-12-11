from uuid import UUID

from sqlmodel import select

from src.models import Subscription
from src.repositories.base_repository import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription

    async def get_subscription(self, subscriber_uuid: UUID, subscribed_uuid: UUID) -> Subscription | None:
        query = select(self.model).where(
            self.model.subscriber_uuid == subscriber_uuid, self.model.subscribed_uuid == subscribed_uuid
        )
        response = await self.session.exec(query)
        return response.one_or_none()
