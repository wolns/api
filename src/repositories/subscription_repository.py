from uuid import UUID

from sqlmodel import select

from src.models import Subscription, User
from src.repositories.base_repository import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription

    async def get_subscription(self, subscriber_uuid: UUID, subscribed_uuid: UUID) -> Subscription | None:
        query = select(Subscription).where(
            Subscription.subscriber_uuid == subscriber_uuid, Subscription.subscribed_uuid == subscribed_uuid
        )
        response = await self.session.exec(query)
        return response.one_or_none()

    async def get_subscriptions(self, user_uuid: UUID) -> list[User]:
        query = (
            select(User)
            .join(Subscription, User.uuid == Subscription.subscribed_uuid)
            .where(Subscription.subscriber_uuid == user_uuid)
        )
        response = await self.session.exec(query)
        return response.all()

    async def get_subscribers(self, user_uuid: UUID) -> list[User]:
        query = (
            select(User)
            .join(Subscription, User.uuid == Subscription.subscriber_uuid)
            .where(Subscription.subscribed_uuid == user_uuid)
        )
        response = await self.session.exec(query)
        return response.all()
