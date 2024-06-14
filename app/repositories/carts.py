from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.core.repository.base import BaseAlchemyRepository
from app.core.repository.schemas_types import ModelType
from app.models.carts import Cart
from app.models.products import Product
from app.schemas.responses.carts import CartCreateResponse

__all__ = [
    'CartRepository',
]


class CartRepository(BaseAlchemyRepository):
    model = Cart
    creation_schema = CartCreateResponse

    async def create(
            self,
            data: dict,
            is_serialize: bool = True,
            **kwargs: Any,
    ) -> ModelType:
        """Добавляет запись в БД."""

        async with self._db.get_session() as session:
            try:
                cart = Cart(user_id=data.get('user_id'))
                db_result = select(Product).options(selectinload(Product.carts)).filter_by(id=data.get("product_id"))
                product = (await session.execute(db_result)).scalar_one()
                product.carts.append(cart)
                await session.commit()
            except SQLAlchemyError as e:
                raise e

            return self.serialize(cart, self.creation_schema) if is_serialize else cart
