from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import ForeignKey
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
    from app.models.users import User

__all__ = [
    'Cart',
    'CartProduct',
]


class CartProduct(Base):
    __tablename__ = 'cart_product'

    cart_id: Mapped[UUID] = mapped_column(
        ForeignKey('cart.id', ondelete='CASCADE'),
        primary_key=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
        primary_key=True,
    )


class Cart(
    Base,
    Creatable,
    Updatable,
    SoftDeletable,
):
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='cart', single_parent=True)

    products: Mapped[List['Product']] = relationship(
        secondary='cart_product',
        back_populates='carts'
    )
