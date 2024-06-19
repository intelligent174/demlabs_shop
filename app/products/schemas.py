from uuid import UUID

from pydantic import BaseModel

from app.core.schemas.responses.common import (
    BaseResponseModel,
    ConfigDictMixin,
)

__all__ = [
    'ProductCreateRequest',
    'ProductFilterRequest',
    'BaseProductResponse',
    'ProductCreateResponse',
    'ProductOnCartResponse',
    'ProductListResponse',
]


class ProductCreateRequest(BaseModel):
    title: str
    description: str
    price: float
    discount: float
    quantity: int
    category_id: UUID


class ProductFilterRequest(BaseModel):
    category_id: UUID


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
