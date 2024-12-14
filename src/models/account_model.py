from typing import ClassVar
from uuid import UUID

from sqlmodel import Field

from src.models.base_model import BaseUUIDModel
from src.schemas.account_schemas import AccountBodySchema
from src.schemas.track_schemas import ServiceType


class BaseAccount(BaseUUIDModel):
    service_type: ClassVar[ServiceType]
    schema: ClassVar[AccountBodySchema]

    user_uuid: UUID = Field(default=None, foreign_key="User.uuid")
