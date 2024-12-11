from fastapi import APIRouter

from .auth.auth import auth_router
from .health_check.health_check import health_check_router
from .tracks.tracks import tracks_router
from .users.users import users_router

subrouters = (
    health_check_router,
    tracks_router,
    users_router,
    auth_router,
)

v1_router = APIRouter(prefix="/v1")

for subrouter in subrouters:
    v1_router.include_router(subrouter)
