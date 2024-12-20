import base64

import aiohttp
from fastapi import HTTPException

from src.core.config import get_spotify_settings
from src.core.exceptions import TokenExpiredException
from src.schemas.account_schemas import SpotifyAccountBodySchema
from src.schemas.track_schemas import ServiceType, TrackBaseInfo
from src.services.music_service import MusicService


class SpotifyService(MusicService):
    service_type = ServiceType.SPOTIFY

    def __init__(self):
        spotify_settings = get_spotify_settings()
        self.client_id = spotify_settings.spotify_client_id
        self.client_secret = spotify_settings.spotify_client_secret
        self.redirect_uri = spotify_settings.spotify_redirect_uri
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"

    def get_auth_url(self) -> str:
        scope = "user-read-currently-playing"
        return (
            f"{self.auth_url}"
            f"?client_id={self.client_id}"
            f"&response_type=code"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scope}"
        )

    async def get_tokens(self, code: str) -> SpotifyAccountBodySchema:
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to get tokens")
                return SpotifyAccountBodySchema.model_validate(await response.json())

    async def get_current_track(self, obj: SpotifyAccountBodySchema) -> TrackBaseInfo | None:
        headers = {"Authorization": f"Bearer {obj.access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_base_url}/me/player/currently-playing", headers=headers) as response:
                if response.status == 401:
                    raise TokenExpiredException

                if response.status == 204:
                    return None

                if response.status != 200:
                    return None

                data = await response.json()
                if not data.get("item"):
                    return None

                if not data["is_playing"]:
                    return None

                return TrackBaseInfo(
                    title=data["item"]["name"],
                    artists=", ".join(artist["name"] for artist in data["item"]["artists"]),
                    cover=data["item"]["album"]["images"][0]["url"],
                    duration_ms=data["item"]["duration_ms"],
                    progress_ms=data.get("progress_ms"),
                )

    async def refresh_tokens(self, refresh_token: str) -> SpotifyAccountBodySchema:
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to refresh token")

                response_data = await response.json()

                if "refresh_token" not in response_data:
                    response_data["refresh_token"] = refresh_token

                return SpotifyAccountBodySchema.model_validate(response_data)


async def get_spotify_service() -> SpotifyService:
    return SpotifyService()
