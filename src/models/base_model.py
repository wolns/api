from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseUUIDModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
