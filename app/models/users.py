from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Optional,
)

from sqlalchemy import (
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.db.columns import (
    SoftDeletable,
    Creatable,
    Updatable,
)
from app.core.db.models import Base

if TYPE_CHECKING:
    from app.models.carts import Cart

__all__ = [
    'User',
]


class User(
    Base,
    Creatable,
    Updatable,
    SoftDeletable,
):
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    patronymic_name: Mapped[str] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    password_salt: Mapped[bytes] = mapped_column(BYTEA, nullable=False)

    cart: Mapped[Optional['Cart']] = relationship(back_populates='user')
