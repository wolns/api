from fastapi import APIRouter

from src.schemas.track_schemas import TrackGetSchema, TracksGetSchema

tracks_router = APIRouter(prefix="/tracks", tags=["Tracks"])


@tracks_router.get("/listening-status")
async def get_listening_status() -> TrackGetSchema:
    """
    Getting random listening status.

    :return:
    """


@tracks_router.get("/listening-statuses")
async def get_listening_statuses() -> TracksGetSchema:
    """
    Getting all listening statuses.

    :return:
    """
