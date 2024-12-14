from celery import Celery
from celery.schedules import crontab

from src.core.config import get_redis_settings
from src.core.timezone import tz

redis_settings = get_redis_settings()

celery_app = Celery(
    "track_updater",
    broker=redis_settings.broker_url,
    # backend=redis_settings.result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=tz,
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "enqueue-user-track-updates-every-minute": {
        "task": "enqueue_user_track_updates",
        "schedule": crontab(minute="*"),
    },
}
