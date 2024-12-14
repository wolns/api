from fastapi import APIRouter, Depends, Query

from src.schemas.account_schemas import YandexMusicAccountBodySchema
from src.schemas.track_schemas import TrackBaseInfo
from src.schemas.yandex_schemas import YandexMusicAuthResponseSchema, YandexMusicCallbackResponseSchema
from src.services.music_services.yandex_music_service import YandexMusicService, get_yandex_music_service

yandex_music_router = APIRouter(prefix="/yandex_music", tags=["Yandex Music"])


# TEST PURPOSES ONLY
@yandex_music_router.get("/current-track")
async def get_current_track(
    access_token: str = Query(...), yandex_music_service: YandexMusicService = Depends(get_yandex_music_service)
) -> TrackBaseInfo:
    test = YandexMusicAccountBodySchema(token=access_token)
    return await yandex_music_service.get_current_track(test)

@yandex_music_router.get("/login", response_model=YandexMusicAuthResponseSchema)
async def yandex_music_login(
    yandex_music_service: YandexMusicService = Depends(get_yandex_music_service)
) -> YandexMusicAuthResponseSchema:
    auth_url = yandex_music_service.get_auth_url()
    return YandexMusicAuthResponseSchema(auth_url=auth_url)


@yandex_music_router.get("/callback")
async def yandex_music_callback(code: str = Query(...), yandex_music_service: YandexMusicService = Depends(get_yandex_music_service)) -> YandexMusicAccountBodySchema:
    return await yandex_music_service.get_tokens(code)
