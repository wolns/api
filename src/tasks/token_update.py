from uuid import UUID

from src.core.celery import celery_app
from src.schemas.track_schemas import ServiceType


@celery_app.task(name="token_update")
def token_update(user_uuid: UUID, refresh_token: str, service_type: ServiceType):
    from src.database.database import async_session
    from src.services.account_service import get_account_service

    async def async_token_update():
        async with async_session() as session:
            account_service = await get_account_service(session)
            if service_type == ServiceType.SPOTIFY:
                await account_service.refresh_spotify_account(user_uuid, refresh_token)
            elif service_type == ServiceType.YANDEX_MUSIC:
                await account_service.refresh_yandex_music_account(user_uuid, refresh_token)

    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_token_update())
