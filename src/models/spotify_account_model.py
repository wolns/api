from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from .account_model import BaseAccount

if TYPE_CHECKING:
    from .user_model import User


class SpotifyAccount(BaseAccount, table=True):
    access_token: str = Field(sa_column=Column(String(400), nullable=False))
    refresh_token: str = Field(sa_column=Column(String(400), nullable=False))

    user: "User" = Relationship(
        back_populates="spotify_account",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
