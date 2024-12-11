from fastapi import APIRouter

from src.schemas.token_schemas import TokenPostBodySchema, TokenPostResponseSchema

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token")
async def post_token(body: TokenPostBodySchema) -> TokenPostResponseSchema:
    """
    Get Token by account data

    :return:
    """
