from pydantic import BaseModel

from src.schemas.user_schemas import UserBaseUUIDSchema


class SubscriptionBaseSchema(UserBaseUUIDSchema):
    pass


class SubscribedGetResponseSchema(BaseModel):
    subscribed: list[SubscriptionBaseSchema]


class SubscribersGetResponseSchema(BaseModel):
    subscribers: list[SubscriptionBaseSchema]
