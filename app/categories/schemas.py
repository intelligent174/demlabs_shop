from pydantic import BaseModel

from app.core.schemas.responses.common import (
    BaseResponseModel,
    ConfigDictMixin,
)

__all__ = [
    'CategoryCreateRequest',
    'CategoryCreateResponse',
]


class CategoryCreateRequest(BaseModel):
    title: str


class CategoryCreateResponse(BaseResponseModel, ConfigDictMixin):
    title: str
