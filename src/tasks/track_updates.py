from uuid import UUID

from src.core.celery import celery_app


@celery_app.task
def update_user_track(user_uuid: UUID):
    from src.database.database import async_session
    from src.services.track_update_service import get_track_update_service

    async def update_track():
        async with async_session() as session:
            track_update_service = await get_track_update_service(session)
            await track_update_service.update_user_track(user_uuid)

    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_track())


@celery_app.task(name="enqueue_user_track_updates")
def enqueue_user_track_updates():
    from src.database.database import async_session
    from src.services.user_service import UserService

    async def enqueue_tasks():
        async with async_session() as session:
            user_service = UserService(session)
            update_track_users = await user_service.get_users_update_track()
            for user in update_track_users:
                update_user_track.delay(user.uuid)

    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(enqueue_tasks())
