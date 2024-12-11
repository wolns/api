from uuid import UUID

from src.models.base_model import BaseModel


class UserBaseSchema(BaseModel):
    name: str
    login: str


class UserBaseUUIDSchema(UserBaseSchema):
    uuid: UUID


class UserResponseSchema(UserBaseUUIDSchema):
    subscribed: list[UserBaseUUIDSchema]
    subscribers: list[UserBaseUUIDSchema]


class UserPostBodySchema(UserBaseSchema):
    password: str
