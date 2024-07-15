from typing import Iterable
from uuid import UUID

from returns.maybe import Maybe
from returns.result import (
    Success,
    Failure,
    ResultE,
)
from sqlalchemy.exc import NoResultFound

from app.core.db.exceptions_types import CastViolationError
from app.categories.exception_messages import CATEGORY_NOT_FOUND
from app.core.service.base import BaseCreateService
from app.products.cache import ProductRedisService
from app.products.exception_messages import (
    PRODUCT_NOT_FOUND,
    PRODUCT_ALREADY_EXISTS,
)
from app.products.models import Product
from app.products.repository import ProductRepository
from app.products.schemas import BaseProductResponse

__all__ = [
    'ProductService',
]


class ProductService(BaseCreateService):
    _errors_map = {
        'NoResultFound': PRODUCT_NOT_FOUND,
        'product_category_id_fkey': CATEGORY_NOT_FOUND,
        'product_title_key': PRODUCT_ALREADY_EXISTS,
    }

    def __init__(
            self,
            repository: ProductRepository,
            cache: ProductRedisService,
    ) -> None:
        super().__init__(repository=repository)
        self.cache = cache

    async def get_by_id(self, product_id: UUID | str) -> Maybe[Product]:
        product_cache = await self.cache.get(key=product_id)

        if product_cache is not None:
            return Success(product_cache)

        try:
            product = await self.repository.get_by_id(product_id)
        except NoResultFound as e:
            error_message = self._errors_map.get(e.__class__.__name__, str(e))
            return Failure(error_message)
        except Exception as e:
            return Failure(str(e))  # type: ignore

        await self.cache.set(key=product_id, data=product)

        return Success(product)

    async def get_list(
            self,
            category_id: UUID,
            is_serialize: bool = True,
    ) -> ResultE[Iterable[BaseProductResponse]]:
        try:
            products = await self.repository.get_list(category_id=category_id, is_serialize=is_serialize)
            return Success(products)
        except CastViolationError as e:
            error_message = self._errors_map.get(e.constraint_name, str(e))
            return Failure(error_message)
        except Exception as e:
            return Failure(str(e))
