from uuid import UUID

from app.schemas.responses import (
    BaseResponseModel,
    ConfigDictMixin,
)

__all__ = [
    'ProductCreateResponse',
    'ProductOnCartResponse',
    'ProductListResponse',
    'BaseProductResponse',
]


class BaseProductResponse(ConfigDictMixin):
    id: UUID
    title: str
    price: float
    discount: float


class ProductCreateResponse(BaseResponseModel, BaseProductResponse):
    description: str
    quantity: int
    category_id: UUID


class ProductOnCartResponse(BaseProductResponse):
    quantity: int


class ProductListResponse(ConfigDictMixin):
    products: list[BaseProductResponse]
