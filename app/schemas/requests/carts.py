from uuid import UUID

from pydantic import BaseModel

__all__ = [
    'CartCreateRequest',
]


class CartCreateRequest(BaseModel):
    product_id: UUID
