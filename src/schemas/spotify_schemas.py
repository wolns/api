from pydantic import BaseModel

# Egor, sorry for this shit ahahahaha


class SpotifyAuthResponseSchema(BaseModel):
    auth_url: str


class SpotifyCallbackResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class SpotifyCurrentTrackResponseSchema(BaseModel):
    title: str
    artists: str
    cover_url: str
    is_playing: bool
