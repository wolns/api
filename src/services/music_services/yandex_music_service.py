import base64
import json
import random
import string

import aiohttp
from fastapi import HTTPException
from yandex_music import ClientAsync

from src.core.config import get_yandex_music_settings
from src.core.exceptions import TokenExpiredException
from src.schemas.account_schemas import YandexMusicAccountBodySchema
from src.schemas.track_schemas import ServiceType, TrackBaseInfo
from src.services.music_service import MusicService


class YandexMusicService(MusicService):
    service_type = ServiceType.YANDEX_MUSIC

    def __init__(self):
        yandex_music_settings = get_yandex_music_settings()
        self.client_id = yandex_music_settings.yandex_music_client_id
        self.client_secret = yandex_music_settings.yandex_music_client_secret
        self.redirect_uri = yandex_music_settings.yandex_music_redirect_uri
        self.auth_url = "https://oauth.yandex.ru/authorize"
        self.token_url = "https://oauth.yandex.ru/token"

    def get_auth_url(self) -> str:
        return (
            f"{self.auth_url}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )

    async def get_tokens(self, code: str) -> YandexMusicAccountBodySchema:
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to get tokens")
                return YandexMusicAccountBodySchema.model_validate(await response.json())

    async def refresh_tokens(self, refresh_token: str) -> YandexMusicAccountBodySchema:
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
                    raise HTTPException(status_code=400, detail="Failed to refresh tokens")
                return YandexMusicAccountBodySchema.model_validate(await response.json())

    # TODO: rewrite
    async def track_from_ynison(self, yandex_music_client: ClientAsync, ynison):
        try:
            track = ynison["player_state"]["player_queue"]["playable_list"][
                ynison["player_state"]["player_queue"]["current_playable_index"]
            ]
        except IndexError:
            return {
                "paused": None,
                "duration_ms": None,
                "progress_ms": None,
                "entity_id": None,
                "entity_type": None,
                "track": None,
            }
        try:
            return {
                "paused": ynison["player_state"]["status"]["paused"],
                "duration_ms": ynison["player_state"]["status"]["duration_ms"],
                "progress_ms": ynison["player_state"]["status"]["progress_ms"],
                "entity_id": ynison["player_state"]["player_queue"]["entity_id"],
                "entity_type": ynison["player_state"]["player_queue"]["entity_type"],
                "track": (await yandex_music_client.tracks(track["playable_id"]))[0],
            }
        except Exception as e:
            print(f"exception {e}, track-id {track['playable_id']}")
            return {
                "paused": ynison["player_state"]["status"]["paused"],
                "duration_ms": ynison["player_state"]["status"]["duration_ms"],
                "progress_ms": ynison["player_state"]["status"]["progress_ms"],
                "entity_id": ynison["player_state"]["player_queue"]["entity_id"],
                "entity_type": ynison["player_state"]["player_queue"]["entity_type"],
                "track": None,
            }

    async def get_preynison(self, yandex_music_token: str):
        device_info = {
            "app_name": "Chrome",
            "type": 1,
        }

        ws_proto = {
            "Ynison-Device-Id": "".join([random.choice(string.ascii_lowercase) for _ in range(16)]),
            "Ynison-Device-Info": json.dumps(device_info),
        }

        session = aiohttp.ClientSession()
        ws = await session.ws_connect(
            url="wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison",
            headers={
                "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(ws_proto)}",
                "Origin": "http://music.yandex.ru",
                "Authorization": f"OAuth {yandex_music_token}",
            },
        )
        recv = await ws.receive()
        data = json.loads(recv.data)

        new_ws_proto = ws_proto.copy()
        if not data["redirect_ticket"]:
            raise TokenExpiredException
        new_ws_proto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

        to_send = {
            "update_full_state": {
                "player_state": {
                    "player_queue": {
                        "current_playable_index": -1,
                        "entity_id": "",
                        "entity_type": "VARIOUS",
                        "playable_list": [],
                        "options": {"repeat_mode": "NONE"},
                        "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                        "version": {
                            "device_id": ws_proto["Ynison-Device-Id"],
                            "version": 9021243204784341000,
                            "timestamp_ms": 0,
                        },
                        "from_optional": "",
                    },
                    "status": {
                        "duration_ms": 0,
                        "paused": True,
                        "playback_speed": 1,
                        "progress_ms": 0,
                        "version": {
                            "device_id": ws_proto["Ynison-Device-Id"],
                            "version": 8321822175199937000,
                            "timestamp_ms": 0,
                        },
                    },
                },
                "device": {
                    "capabilities": {
                        "can_be_player": True,
                        "can_be_remote_controller": False,
                        "volume_granularity": 16,
                    },
                    "info": {
                        "device_id": ws_proto["Ynison-Device-Id"],
                        "type": "WEB",
                        "title": "Chrome Browser",
                        "app_name": "Chrome",
                    },
                    "volume_info": {"volume": 0},
                    "is_shadow": True,
                },
                "is_currently_active": False,
            },
            "rid": "ac281c26-a047-4419-ad00-e4fbfda1cba3",
            "player_action_timestamp_ms": 0,
            "activity_interception_type": "DO_NOT_INTERCEPT_BY_DEFAULT",
        }

        return session, to_send, data["host"], json.dumps(new_ws_proto)

    async def get_current_track(self, obj: YandexMusicAccountBodySchema) -> TrackBaseInfo | None:
        session, to_send, host, proto = await self.get_preynison(obj.access_token)
        async with session.ws_connect(
            url=f"wss://{host}/ynison_state.YnisonStateService/PutYnisonState",
            headers={
                "Sec-WebSocket-Protocol": f"Bearer, v2, {proto}",
                "Origin": "http://music.yandex.ru",
                "Authorization": f"OAuth {obj.access_token}",
            },
            method="GET",
        ) as ws:
            await ws.send_str(json.dumps(to_send))
            recv = await ws.receive()
            await session.close()
            ynison = json.loads(recv.data)
            yandex_music_client = ClientAsync(token=obj.access_token)
            await yandex_music_client.init()
            track = await self.track_from_ynison(yandex_music_client, ynison)

            if not track or not track["track"]:
                return None

            if track["paused"]:
                return None

            return TrackBaseInfo(
                title=track["track"].title,
                artists=", ".join(x.name for x in track["track"].artists),
                cover="https://" + track["track"].cover_uri.replace("%%", "400x400"),
                duration_ms=track["duration_ms"],
            )


async def get_yandex_music_service() -> YandexMusicService:
    return YandexMusicService()
