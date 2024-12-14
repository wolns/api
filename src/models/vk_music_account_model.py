from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.schemas.account_schemas import VkMusicAccountBodySchema, AccountBodySchema
from src.schemas.track_schemas import ServiceType
from .account_model import BaseAccount

if TYPE_CHECKING:
    from .user_model import User


class VkMusicAccount(BaseAccount, table=True):
    service_type: ClassVar[ServiceType] = ServiceType.VK_MUSIC
    schema: ClassVar[AccountBodySchema] = VkMusicAccountBodySchema

    access_token: str = Field(sa_column=Column(String(400), nullable=False))

    user: "User" = Relationship(
        back_populates="vk_music_account",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
