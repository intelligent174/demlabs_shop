from typing import Iterable

from pydantic import BaseModel

from app.schemas.responses import (
    BaseResponseModel,
    ConfigDictMixin,
)

__all__ = [
    'CategoryCreateResponse',
    'CategoryListResponse',
]


class CategoryCreateResponse(BaseResponseModel, ConfigDictMixin):
    title: str


class CategoryListResponse(BaseModel):
    categories: Iterable[CategoryCreateResponse]
