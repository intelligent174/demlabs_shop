from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from app.core.db.columns import (
    SoftDeletable,
    Creatable,
    Updatable,
)
from app.core.db.models import Base

if TYPE_CHECKING:
    from app.models.products import Product

__all__ = [
    'Category',
]


class Category(
    Base,
    Creatable,
    Updatable,
    SoftDeletable,
):
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    products: Mapped[Optional[List['Product']]] = relationship(back_populates='category')
