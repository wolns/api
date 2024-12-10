from fastapi import APIRouter

from .v1 import v1_router

subrouters = (v1_router,)

api_router = APIRouter(prefix="/api")

for subrouter in subrouters:
    api_router.include_router(subrouter)
