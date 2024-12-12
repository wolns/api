from datetime import datetime, timedelta
from uuid import UUID

import jwt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from src.core.config import JWTSettings
from src.core.timezone import tz


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz) + timedelta(days=1)
    to_encode.update({"exp": int(expire.timestamp())})

    jwt_settings = JWTSettings()
    return jwt.encode(to_encode, jwt_settings.jwt_secret, algorithm=jwt_settings.jwt_algorithm)


def verify_access_token(token: str) -> dict:
    jwt_settings = JWTSettings()
    try:
        return jwt.decode(token, jwt_settings.jwt_secret, algorithms=[jwt_settings.jwt_algorithm])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


security = HTTPBearer()


async def get_current_user_uuid(authorization: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    token = authorization.credentials
    return UUID(verify_access_token(token)["user_uuid"])
