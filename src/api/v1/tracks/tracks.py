from fastapi import APIRouter

tracks_router = APIRouter(prefix="/tracks", tags=["Tracks"])


@tracks_router.get("/listening-status")
async def get_listening_status():
    """
    Getting random listening status.

    :return:
    """


@tracks_router.get("/listening-statuses")
async def get_listening_statuses():
    """
    Getting all listening statuses.

    :return:
    """
