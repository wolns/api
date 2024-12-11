from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.schemas.user_schemas import UserPostBodySchema, UserResponseSchema
from src.services.user_service import UserService, get_user_service
from src.utils.jwt import get_current_user_uuid

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def register_user(
    data: UserPostBodySchema, user_service: UserService = Depends(get_user_service)
) -> UserResponseSchema:
    """
    User registration

    :return:
    """
    user = await user_service.register_user(data)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return await user_service.to_response_schema(user)


@users_router.get("/me")
async def get_me(
    user_uuid: UUID = Depends(get_current_user_uuid), user_service: UserService = Depends(get_user_service)
) -> UserResponseSchema:
    """
    Get user information
    TOKEN Required

    :return:
    """
    user = await user_service.get_user_by_uuid(user_uuid)
    return await user_service.to_response_schema(user)


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
