from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr, validates
from sqlmodel import Field, SQLModel

from src.core.timezone import tz


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseUUIDModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(tz),
    )
    updated_at: datetime = Field(sa_type=DateTime(timezone=True), default_factory=lambda: datetime.now(tz))

    @validates("updated_at")
    def validate_updated_at(self, key, value):
        return datetime.now(tz)
