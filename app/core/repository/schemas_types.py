from typing import TypeVar

from pydantic import BaseModel as BaseModelSchema
from app.core.db.models import Base

ModelType = TypeVar('ModelType', bound=Base)
BaseSchemaType = TypeVar('BaseSchemaType', bound=BaseModelSchema)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModelSchema)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModelSchema)
GetSchemaType = TypeVar('GetSchemaType', bound=BaseModelSchema)
