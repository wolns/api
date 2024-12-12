import random
from datetime import datetime, timedelta
from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.timezone import tz
from src.database.database import get_async_session
from src.models.track_model import Track
from src.schemas.track_schemas import TrackGetResponseSchema
from src.services.subscription_service import SubscriptionService
from src.services.track_service import TrackService
from src.services.user_service import UserService


class TrackBusinessService:
    def __init__(
        self, track_service: TrackService, user_service: UserService, subscription_service: SubscriptionService
    ):
        self.track_service = track_service
        self.user_service = user_service
        self.subscription_service = subscription_service

    async def get_subscribed_tracks_by_user_uuid(self, user_uuid: UUID) -> list[Track]:
        subscribed_users = await self.subscription_service.get_subscribed(user_uuid)

        subscribed_tracks = []
        for subscribed_user in subscribed_users:
            track = await self.track_service.get_track_by_user_uuid(subscribed_user.uuid)
            if track:
                subscribed_tracks.append(track)

        return subscribed_tracks

    async def get_subscribed_recently_tracks_by_user_uuid(self, user_uuid: UUID) -> list[Track]:
        subscribed_users = await self.subscription_service.get_subscribed(user_uuid)

        recent_tracks = []
        for subscribed_user in subscribed_users:
            track = await self.track_service.get_recently_updated_track_by_user_uuid(subscribed_user.uuid)
            if track:
                recent_tracks.append(track)

        return recent_tracks

    async def get_subscribed_track_by_user_uuid(self, user_uuid: UUID) -> Track:
        recent_tracks = await self.get_subscribed_recently_tracks_by_user_uuid(user_uuid)
        if len(recent_tracks) > 0:
            return random.choice(recent_tracks)  # noqa: S311

        subscribed_users = await self.subscription_service.get_subscribed(user_uuid)
        random_subscribed = random.choice(subscribed_users)  # noqa: S311
        return await self.track_service.get_track_by_user_uuid(random_subscribed.uuid)

    async def to_response_model(self, track: Track) -> TrackGetResponseSchema:
        threshold_time = datetime.now(tz) - timedelta(minutes=1)
        is_playing = track.updated_at > threshold_time
        return TrackGetResponseSchema(
            user_name=track.user.name,
            is_playing=is_playing,
            service_type=track.service_type,
            title=track.title,
            artists=track.artists,
            cover=track.cover,
        )


async def get_track_business_service(session: AsyncSession = Depends(get_async_session)):
    track_service = TrackService(session)
    user_service = UserService(session)
    subscription_service = SubscriptionService(session)
    return TrackBusinessService(track_service, user_service, subscription_service)
