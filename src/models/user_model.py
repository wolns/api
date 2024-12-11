from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .spotify_account_model import SpotifyAccount
    from .subscription_model import Subscription
    from .vk_music_account_model import VkMusicAccount
    from .yandex_music_account_model import YandexMusicAccount


class User(BaseUUIDModel, table=True):
    name: str = Field(sa_column=Column(String(100), nullable=False))
    login: str = Field(sa_column=Column(String(100), nullable=False))
    hashed_password: str = Field(sa_column=Column(String(100), nullable=True))

    follows: list["Subscription"] = Relationship(back_populates="follower", sa_relationship_kwargs={"lazy": "selectin"})
    followers: list["Subscription"] = Relationship(
        back_populates="followes", sa_relationship_kwargs={"lazy": "selectin"}
    )

    yandex_music_account_uuid: UUID = Field(default=None, foreign_key="YandexMusicAccount.uuid")
    yandex_music_account: "YandexMusicAccount" = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )

    spotify_account_uuid: UUID = Field(default=None, foreign_key="SpotifyAccount.uuid")
    spotify_account: "SpotifyAccount" = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )

    vk_music_account_uuid: UUID = Field(default=None, foreign_key="VkMusicAccount.uuid")
    vk_music_account: "VkMusicAccount" = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
