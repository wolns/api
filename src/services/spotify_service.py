import base64

import aiohttp
from fastapi import HTTPException

from src.core.config import get_settings
from src.schemas.spotify_schemas import SpotifyCurrentTrackResponseSchema


class SpotifyService:
    def __init__(self):
        settings = get_settings()
        self.client_id = settings.spotify_client_id
        self.client_secret = settings.spotify_client_secret
        self.redirect_uri = settings.spotify_redirect_uri
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"

    def get_auth_url(self) -> str:
        scope = "user-read-currently-playing"
        auth_url = (
            f"{self.auth_url}"
            f"?client_id={self.client_id}"
            f"&response_type=code"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scope}"
        )
        return auth_url

    async def get_tokens(self, code: str) -> dict:
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
                return await response.json()

    async def get_current_track(self, access_token: str) -> SpotifyCurrentTrackResponseSchema | None:
        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_base_url}/me/player/currently-playing", headers=headers) as response:
                if response.status == 204:
                    return None

                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to get current track")

                data = await response.json()
                if not data.get("item"):
                    return None

                return SpotifyCurrentTrackResponseSchema(
                    title=data["item"]["name"],
                    artists=", ".join(artist["name"] for artist in data["item"]["artists"]),
                    cover_url=data["item"]["album"]["images"][0]["url"],
                    is_playing=data["is_playing"],
                )


async def get_spotify_service() -> SpotifyService:
    return SpotifyService()
