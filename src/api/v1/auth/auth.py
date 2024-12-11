from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.schemas.token_schemas import TokenPostBodySchema, TokenPostResponseSchema
from src.services.user_service import UserService, get_user_service
from src.utils.jwt import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token")
async def post_token(
    obj: TokenPostBodySchema, user_service: UserService = Depends(get_user_service)
) -> TokenPostResponseSchema:
    """
    Get Token by account data

    :return:
    """
    user = await user_service.login_user(obj)
    if not user:
        raise HTTPException(status_code=400, detail="User not exists")
    return TokenPostResponseSchema(access_token=create_access_token({"user_uuid": str(user.uuid)}))
