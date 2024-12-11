from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def create_user():
    """
    User registration
    :return:
    """


@users_router.get("/me")
async def get_me():
    """
    Get user information
    TOKEN Required

    :return:
    """
