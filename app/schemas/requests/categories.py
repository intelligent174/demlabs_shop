from pydantic import BaseModel

__all__ = [
    'CategoryCreateRequest',
]


class CategoryCreateRequest(BaseModel):
    title: str
