from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models import Subscription, User
from src.repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self, session: AsyncSession):
        self.subscription_repository = SubscriptionRepository(session)

    async def subscribe(self, subscriber_uuid: UUID, subscribed_uuid: UUID) -> bool:
        if subscriber_uuid == subscribed_uuid:
            return False

        existing_subscription = await self.subscription_repository.get_subscription(subscriber_uuid, subscribed_uuid)
        if existing_subscription:
            return False

        subscription = Subscription(subscriber_uuid=subscriber_uuid, subscribed_uuid=subscribed_uuid)
        await self.subscription_repository.add(subscription)
        return True

    async def unsubscribe(self, subscriber_uuid: UUID, subscribed_uuid: UUID) -> bool:
        subscription = await self.subscription_repository.get_subscription(subscriber_uuid, subscribed_uuid)
        if not subscription:
            return False

        await self.subscription_repository.delete(subscription)
        return True

    async def get_subscribed(self, user_uuid: UUID) -> list[User]:
        return await self.subscription_repository.get_subscribed(user_uuid)

    async def get_subscribers(self, user_uuid: UUID) -> list[User]:
        return await self.subscription_repository.get_subscribers(user_uuid)


async def get_subscriptions_service(session: AsyncSession = Depends(get_async_session)) -> SubscriptionService:
    return SubscriptionService(session)
