from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel
from src.schemas.track_schemas import ServiceType

if TYPE_CHECKING:
    from .user_model import User


class Track(BaseUUIDModel, table=True):
    is_playing: bool = Field(default=True, nullable=False)
    service_type: ServiceType = Field(nullable=False)

    title: str = Field(sa_column=Column(String(100), nullable=False))
    artists: str = Field(sa_column=Column(String(100), nullable=False))
    cover: str = Field(sa_column=Column(String(200), nullable=False))

    user_uuid: UUID = Field(default=None, foreign_key="User.uuid")
    user: "User" = Relationship(
        back_populates="track",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
