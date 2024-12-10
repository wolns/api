from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .friend_model import Friend


class User(BaseUUIDModel, table=True):
    name: str = Field(sa_column=Column(String(100), nullable=False))
    login: str = Field(sa_column=Column(String(100), nullable=False))
    hashed_password: str = Field(sa_column=Column(String(100), nullable=True))

    follows: list["Friend"] = Relationship(back_populates="follower", sa_relationship_kwargs={"lazy": "selectin"})
    followers: list["Friend"] = Relationship(back_populates="followes", sa_relationship_kwargs={"lazy": "selectin"})
