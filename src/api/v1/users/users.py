from fastapi import APIRouter

from src.schemas.user_schemas import UserGetResponseSchema, UserPostResponseSchema

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def create_user() -> UserPostResponseSchema:
    """
    User registration
    :return:
    """


@users_router.get("/me")
async def get_me() -> UserGetResponseSchema:
    """
    Get user information
    TOKEN Required

    :return:
    """
