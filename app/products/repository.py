from typing import Iterable
from uuid import UUID

from returns.result import ResultE
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.repository.base import BaseAlchemyRepository
from app.products.models import Product
from app.products.schemas import (
    ProductCreateResponse,
    BaseProductResponse,
)

__all__ = [
    'ProductRepository',
]


class ProductRepository(BaseAlchemyRepository):
    model = Product
    creation_schema = ProductCreateResponse
    getion_schema = BaseProductResponse

    async def get_list(  # noqa
            self,
            category_id: UUID,
            is_serialize: bool = True,
    ) -> ResultE[Iterable[BaseProductResponse]]:
        query = (
            select(self.model)
            .where(self.model.category_id == category_id)
        )

        async with self._db.get_session() as session:
            try:
                db_result = await session.execute(query)
                instances = db_result.scalars()
            except SQLAlchemyError as e:
                raise e

            return self.serialize_many(instances, self.getion_schema) if is_serialize else instances
