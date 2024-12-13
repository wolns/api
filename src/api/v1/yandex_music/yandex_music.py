from fastapi import APIRouter, Depends, Query

from src.schemas.account_schemas import YandexMusicAccountBodySchema
from src.schemas.track_schemas import TrackBaseInfo
from src.services.music_services.yandex_music_service import YandexMusicService, get_yandex_music_service

yandex_music_router = APIRouter(prefix="/yandex_music", tags=["Yandex Music"])


# TEST PURPOSES ONLY
@yandex_music_router.get("/current-track")
async def get_current_track(
    access_token: str = Query(...), yandex_music_service: YandexMusicService = Depends(get_yandex_music_service)
) -> TrackBaseInfo:
    test = YandexMusicAccountBodySchema(token=access_token)
    return await yandex_music_service.get_current_track(test)
