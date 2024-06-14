from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

__all__ = [
    'CreatableBy',
    'UpdatableBy',
    'Creatable',
    'Updatable',
    'SoftDeletable',
    'TimeZoneOffset',
]


class CreatableBy:
    created_by = Column(UUID, nullable=True)


class UpdatableBy:
    updated_by = Column(UUID, nullable=True)


class Creatable:
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )


class Updatable:
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class SoftDeletable:
    deleted_at = Column(DateTime, nullable=True)


class TimeZoneOffset:
    utc_offset = Column(Integer, nullable=True)
