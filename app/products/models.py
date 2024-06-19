from typing import TYPE_CHECKING, List

from sqlalchemy import (
    String,
    Numeric,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
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
    from app.categories.models import Category
    from app.carts.models import Cart

__all__ = [
    'Product',
]


class Product(
    Base,
    Creatable,
    Updatable,
    SoftDeletable,
):
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(9, 2), nullable=False)
    discount: Mapped[float] = mapped_column(Numeric(9, 2), default=0.0)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    category_id: Mapped[UUID] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship(back_populates='products')
    carts: Mapped[List['Cart']] = relationship(secondary='cart_product', back_populates='products')
