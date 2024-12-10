from fastapi import APIRouter

health_check_router = APIRouter(prefix="/health_check", tags=["Health Check"])


@health_check_router.get("/")
async def health_check():
    return {"status": "ok"}
