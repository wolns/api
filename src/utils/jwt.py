from datetime import datetime, timedelta

import jwt

from src.core.config import get_settings
from src.database.database import settings


def sign_jwt(user_uuid: str) -> str:
    payload = {"user_uuid": user_uuid, "expires": (datetime.now() + timedelta(days=1)).isoformat()}
    settings = get_settings()
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return decoded_token if datetime.fromisoformat(decoded_token["expires"]) >= datetime.now() else None
    except:
        return {}
