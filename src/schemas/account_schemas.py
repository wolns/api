from pydantic import BaseModel


class AccountBodySchema(BaseModel):
    pass


class YandexMusicAccountBodySchema(AccountBodySchema):
    token: str


class SpotifyAccountBodySchema(AccountBodySchema):
    access_token: str
    refresh_token: str


class VkMusicAccountBodySchema(AccountBodySchema):
    token: str
