from fastapi import APIRouter, Depends, Query

from src.schemas.account_schemas import SpotifyAccountBodySchema
from src.schemas.spotify_schemas import (
    SpotifyAuthResponseSchema,
    SpotifyCallbackResponseSchema,
)
from src.schemas.track_schemas import TrackBaseInfo
from src.services.music_services.spotify_service import SpotifyService, get_spotify_service

spotify_router = APIRouter(prefix="/spotify", tags=["Spotify"])


@spotify_router.get("/login")
async def spotify_login(spotify_service: SpotifyService = Depends(get_spotify_service)) -> SpotifyAuthResponseSchema:
    auth_url = spotify_service.get_auth_url()
    return SpotifyAuthResponseSchema(auth_url=auth_url)


@spotify_router.get("/callback")
async def spotify_callback(
    code: str = Query(...), spotify_service: SpotifyService = Depends(get_spotify_service)
) -> SpotifyCallbackResponseSchema:
    tokens = await spotify_service.get_tokens(code)
    return SpotifyCallbackResponseSchema(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
    )


# TEST PURPOSES ONLY
@spotify_router.get("/current-track")
async def get_current_track(
    access_token: str = Query(...), spotify_service: SpotifyService = Depends(get_spotify_service)
) -> TrackBaseInfo:
    test = SpotifyAccountBodySchema(access_token=access_token, refresh_token=access_token)
    return await spotify_service.get_current_track(test)
