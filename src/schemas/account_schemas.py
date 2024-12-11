from pydantic import BaseModel


class AccountBodySchema(BaseModel):
    pass


class YandexMusicAccountBodySchema(AccountBodySchema):
    token: str


class SpotifyAccountBodySchema(AccountBodySchema):
    token: str
    refresh_token: str


class VkMusicAccountBodySchema(AccountBodySchema):
    token: str
