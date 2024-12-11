from pydantic import BaseModel


class YandexMusicAccountBodySchema(BaseModel):
    token: str


class SpotifyAccountBodySchema(BaseModel):
    token: str
    refresh_token: str


class VkMusicAccountBodySchema(BaseModel):
    token: str
