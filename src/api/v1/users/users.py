from uuid import UUID

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


@users_router.post("/{user_uuid}/subscribe")
async def post_subscribe(user_uuid: UUID):
    """
    Subscribe a user

    :param user_uuid:
    :return:
    """


@users_router.delete("/{user_uuid}/subscribe")
async def delete_subscribe(user_uuid: UUID):
    """
    Unsubscribe a user

    :param user_uuid:
    :return:
    """
