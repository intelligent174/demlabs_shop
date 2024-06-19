from typing import Iterable
from uuid import UUID

from returns.result import (
    Success,
    Failure,
    ResultE,
)

from app.core.db.exceptions_types import CastViolationError
from app.core.service.base import BaseCreateService
from app.categories.exception_messages import CATEGORY_NOT_FOUND
from app.products.exception_messages import (
    PRODUCT_NOT_FOUND,
    PRODUCT_ALREADY_EXISTS,
)
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
