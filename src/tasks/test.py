"""
EXAMPLE TASKS
@celery_app.task
def update_user_tracks_batch():
    print("hello")


@celery_app.task
def update_user_track(user_uuid: str, service_type: str):
    print(f"{user_uuid}, {service_type}")
"""
