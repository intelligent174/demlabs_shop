from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

__all__ = [
    'BaseResponseModel',
    'ConfigDictMixin',
]


class ConfigDictMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
