from pydantic import BaseModel


class AccountBodySchema(BaseModel):
    pass


class YandexMusicAccountBodySchema(AccountBodySchema):
    access_token: str
    refresh_token: str


class SpotifyAccountBodySchema(AccountBodySchema):
    access_token: str
    refresh_token: str


class VkMusicAccountBodySchema(AccountBodySchema):
    access_token: str
