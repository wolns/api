from fastapi import APIRouter, Depends, Query

from src.schemas.spotify_schemas import (
    SpotifyAuthResponseSchema,
    SpotifyCallbackResponseSchema,
    SpotifyCurrentTrackResponseSchema,
)
from src.services.spotify_service import SpotifyService, get_spotify_service

spotify_router = APIRouter(prefix="/spotify", tags=["Spotify"])


@spotify_router.get("/login", response_model=SpotifyAuthResponseSchema)
async def spotify_login(spotify_service: SpotifyService = Depends(get_spotify_service)) -> SpotifyAuthResponseSchema:
    auth_url = spotify_service.get_auth_url()
    return SpotifyAuthResponseSchema(auth_url=auth_url)


@spotify_router.get("/callback", response_model=SpotifyCallbackResponseSchema)
async def spotify_callback(
    code: str = Query(...), spotify_service: SpotifyService = Depends(get_spotify_service)
) -> SpotifyCallbackResponseSchema:
    tokens = await spotify_service.get_tokens(code)
    return SpotifyCallbackResponseSchema(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
    )


@spotify_router.get("/current-track", response_model=SpotifyCurrentTrackResponseSchema)
async def get_current_track(
    access_token: str = Query(...), spotify_service: SpotifyService = Depends(get_spotify_service)
) -> SpotifyCurrentTrackResponseSchema:
    return await spotify_service.get_current_track(access_token)
