from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token")
async def post_token():
    """
    Get Token by account data

    :return:
    """
