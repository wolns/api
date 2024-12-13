from pydantic import BaseModel


class SpotifyAuthResponseSchema(BaseModel):
    auth_url: str


class SpotifyCallbackResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
