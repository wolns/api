from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User


class VkMusicAccount(BaseUUIDModel, table=True):
    token: str = Field(sa_column=Column(String(100), nullable=False))

    user_uuid: UUID = Field(default=None, foreign_key="User.uuid")
    user: "User" = Relationship(back_populates="vk_music_account", sa_relationship_kwargs={"lazy": "selectin"})
