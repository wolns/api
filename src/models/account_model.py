from uuid import UUID

from sqlmodel import Field

from src.models.base_model import BaseUUIDModel


class BaseAccount(BaseUUIDModel):
    user_uuid: UUID = Field(default=None, foreign_key="User.uuid")
