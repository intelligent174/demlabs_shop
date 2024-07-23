from typing import Generic
from uuid import UUID

from orjson.orjson import loads
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.core.repository.schemas_types import GetSchemaType

__all__ = [
    'BaseRedisService',
]


class BaseRedisService(
    Generic[
        GetSchemaType,
    ],
):
    getion_schema: GetSchemaType = NotImplemented

    __service_key__: str = NotImplemented

    def __init__(self, redis_pool: Redis) -> None:  # type: ignore
        self._redis_pool = redis_pool

    async def get(self, key: UUID) -> GetSchemaType | None:
        cached_data = await self._redis_pool.get(self._format_key(key))
        return cached_data if cached_data is None else self._serialize(cached_data)

    async def set(
            self,
            key: UUID,
            data: GetSchemaType,
            expire: ExpiryT | None = None
    ) -> None:
        await self._redis_pool.set(
            name=self._format_key(key),
            value=data.model_dump_json(),
            ex=expire,
        )

    def _format_key(self, key: UUID) -> str:
        return f'{self.__service_key__}:{key}'

    def _serialize(self, row: str | bytes) -> GetSchemaType:
        return self.getion_schema(**loads(row))  # noqa
