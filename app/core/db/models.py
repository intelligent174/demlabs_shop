from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy.dialects.postgresql import UUID

__all__ = [
    'Base',
]


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
