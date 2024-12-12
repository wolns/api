from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.schemas.track_schemas import TrackGetResponseSchema, TracksGetResponseSchema
from src.services.track_business_service import TrackBusinessService, get_track_business_service
from src.utils.jwt import get_current_user_uuid

tracks_router = APIRouter(prefix="/tracks", tags=["Tracks"])


@tracks_router.get("/listening-status")
async def get_listening_status(
    current_user_uuid: UUID = Depends(get_current_user_uuid),
    track_business_service: TrackBusinessService = Depends(get_track_business_service),
) -> TrackGetResponseSchema:
    """
    Getting random listening status.

    :return:
    """
    track = await track_business_service.get_subscribed_track_by_user_uuid(current_user_uuid)
    if track:
        return await track_business_service.to_response_model(track)
    raise HTTPException(detail="Track not found", status_code=404)


@tracks_router.get("/listening-statuses")
async def get_listening_statuses(
    current_user_uuid: UUID = Depends(get_current_user_uuid),
    track_business_service: TrackBusinessService = Depends(get_track_business_service),
) -> TracksGetResponseSchema:
    """
    Getting all listening statuses.

    :return:
    """
    tracks = await track_business_service.get_subscribed_tracks_by_user_uuid(current_user_uuid)
    return TracksGetResponseSchema(tracks=[await track_business_service.to_response_model(track) for track in tracks])
