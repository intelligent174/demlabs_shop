from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

__all__ = [
    'CreatableBy',
    'UpdatableBy',
    'Creatable',
    'Updatable',
    'SoftDeletable',
    'TimeZoneOffset',
]


class CreatableBy:
    created_by: Mapped[UUID] = mapped_column(UUID, nullable=True)


class UpdatableBy:
    updated_by: Mapped[UUID] = mapped_column(UUID, nullable=True)


class Creatable:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )


class Updatable:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class SoftDeletable:
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class TimeZoneOffset:
    utc_offset: Mapped[int] = mapped_column(Integer, nullable=True)
