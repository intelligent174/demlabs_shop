from typing import Iterable
from uuid import UUID

from pydantic import BaseModel

from app.core.schemas.responses.common import ConfigDictMixin
from app.products.schemas import ProductOnCartResponse

__all__ = [
    'CartCreateRequest',
    'CartCreateResponse',
]


class CartCreateRequest(BaseModel):
    product_id: UUID


class CartCreateResponse(ConfigDictMixin):
    id: UUID
    products: Iterable[ProductOnCartResponse]
