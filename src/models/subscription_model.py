from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User


class Subscription(BaseUUIDModel, table=True):
    subscriber_uuid: UUID = Field(default=None, foreign_key="User.uuid")
    subscriber: "User" = Relationship(
        back_populates="subscribed",
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Subscription.subscriber_uuid"},
    )

    subscribed_uuid: UUID = Field(default=None, foreign_key="User.uuid")
    subscribed: "User" = Relationship(
        back_populates="subscribers",
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Subscription.subscribed_uuid"},
    )
