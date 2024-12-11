from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models import User
from src.repositories.user_repository import UserRepository
from src.schemas.user_schemas import UserBaseUUIDSchema, UserPostBodySchema, UserResponseSchema
from src.utils.security import get_plain_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def register_user(self, obj: UserPostBodySchema) -> User | None:
        user = await self.user_repository.get_by_login(obj.login)
        if user:
            return None
        user = User(name=obj.name, login=obj.login, hashed_password=get_plain_hash(obj.password))
        return await self.user_repository.add(user)

    async def to_response_schema(self, user: User) -> UserResponseSchema:
        return UserResponseSchema(
            uuid=user.uuid,
            name=user.name,
            login=user.login,
            subscribed=[UserBaseUUIDSchema.model_validate(sub) for sub in user.subscribed],
            subscribers=[UserBaseUUIDSchema.model_validate(sub) for sub in user.subscribers],
        )


async def get_user_service(session: AsyncSession = Depends(get_async_session)):
    return UserService(session)
