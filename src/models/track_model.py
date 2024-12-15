from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String, Integer
from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel
from src.schemas.track_schemas import ServiceType

if TYPE_CHECKING:
    from .user_model import User


class Track(BaseUUIDModel, table=True):
    service_type: ServiceType = Field(nullable=False)

    title: str = Field(sa_column=Column(String(100), nullable=False))
    artists: str = Field(sa_column=Column(String(100), nullable=False))
    cover: str = Field(sa_column=Column(String(200), nullable=False))
    duration_ms: int = Field(sa_column=Column(Integer, nullable=True))

    user_uuid: UUID = Field(default=None, foreign_key="User.uuid")
    user: "User" = Relationship(
        back_populates="track",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
