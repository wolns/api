from pydantic import BaseModel


class YandexMusicAuthResponseSchema(BaseModel):
    auth_url: str


class YandexMusicRefreshTokenSchema(BaseModel):
    refresh_token: str


class YandexMusicCallbackResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
