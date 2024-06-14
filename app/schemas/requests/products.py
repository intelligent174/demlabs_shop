from uuid import UUID

from pydantic import BaseModel

__all__ = [
    'ProductCreateRequest',
    'ProductFilterRequest',
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
