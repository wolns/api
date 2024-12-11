from typing import TYPE_CHECKING

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

    subscribed: list["Subscription"] = Relationship(
        back_populates="subscriber",
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Subscription.subscriber_uuid"},
    )
    subscribers: list["Subscription"] = Relationship(
        back_populates="subscribed",
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Subscription.subscribed_uuid"},
    )

    yandex_music_account: "YandexMusicAccount" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    spotify_account: "SpotifyAccount" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    vk_music_account: "VkMusicAccount" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
