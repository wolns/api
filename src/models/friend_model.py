from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User


class Friend(BaseUUIDModel):
    follower_uuid: UUID = Field(default=None, foreign_key="user.uuid")
    follower: "User" = Relationship(back_populates="follows", sa_relationship_kwargs={"lazy": "selectin"})

    followes_uuid: UUID = Field(default=None, foreign_key="user.uuid")
    followes: "User" = Relationship(back_populates="followers", sa_relationship_kwargs={"lazy": "selectin"})
