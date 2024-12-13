from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseUUIDModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_on: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )
