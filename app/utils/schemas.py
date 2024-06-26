from typing import (
    Any,
    Iterable,
)
from uuid import UUID

from fastapi import Response
from orjson.orjson import dumps
from pydantic import BaseModel


class CustomJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: BaseModel | Iterable[BaseModel] | Any):

        if isinstance(content, BaseModel):
            return content.model_dump_json().encode(self.charset)
        elif isinstance(content, list):
            return dumps([  # TODO: orjson.dumps vs Pydantic 2 (решения из коробки)
                item.model_dump()
                for item in content
            ],
                default=self._uuid_decoder
            )

    @staticmethod
    def _uuid_decoder(schema_field: Any) -> str:
        if isinstance(schema_field, UUID):
            return str(schema_field)
