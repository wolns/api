from fastapi import APIRouter

from src.schemas.user_schemas import UserGetSchema, UserPostSchema

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def create_user() -> UserPostSchema:
    """
    User registration
    :return:
    """


@users_router.get("/me")
async def get_me() -> UserGetSchema:
    """
    Get user information
    TOKEN Required

    :return:
    """
