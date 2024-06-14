from typing import Iterable
from uuid import UUID

from app.schemas.responses import ConfigDictMixin
from app.schemas.responses.products import ProductOnCartResponse

__all__ = [
    'CartCreateResponse',
]


class CartCreateResponse(ConfigDictMixin):
    id: UUID
    products: Iterable[ProductOnCartResponse]
