from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseUUIDModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
