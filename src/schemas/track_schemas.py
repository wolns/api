from enum import Enum

from src.models.base_model import BaseModel


class ServiceType(str, Enum):
    YANDEX_MUSIC = "yandex_music"
    SPOTIFY = "spotify"
    VK_MUSIC = "vk_music"


class TrackBaseInfo(BaseModel):
    title: str
    artists: str
    cover: str
    duration_ms: int | None = None
    progress_ms: int | None = None


class TrackBaseSchema(TrackBaseInfo):
    user_name: str
    is_playing: bool
    service_type: ServiceType


class TrackGetResponseSchema(TrackBaseSchema):
    pass


class TracksGetResponseSchema(BaseModel):
    tracks: list[TrackGetResponseSchema]
