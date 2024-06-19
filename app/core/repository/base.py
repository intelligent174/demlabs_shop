from typing import Any, Iterable, Type
from uuid import UUID

from returns.result import ResultE
from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.exc import SQLAlchemyError

from app.core.db.base import Database
from app.core.repository.schemas_types import (
    ModelType,
    SchemaType,
    CreateSchemaType,
)


class BaseAlchemyRepository:
    """Базовый класс репозитория для работы с SQLAlchemy"""
    model: Type[ModelType] = NotImplemented
    creation_schema: CreateSchemaType = NotImplemented

    def __init__(self, db_demlabs_shop: Database) -> None:
        self._db = db_demlabs_shop

    async def create(
            self,
            data: dict,
            is_serialize: bool = True,
            **kwargs: Any,
    ) -> ModelType:
        """Добавляет запись в БД."""
        stmt = (
            insert(self.model)
            .values(**data, **kwargs)
            .returning(self.model)
        )

        async with self._db.get_session() as session:
            try:
                instance = await session.scalar(stmt)
                await session.commit()
            except SQLAlchemyError as e:
                raise e.orig.__cause__  # type: ignore

            return self.serialize(instance) if is_serialize else instance

    async def get_by_id(
            self,
            instance_id: UUID,
            is_serialize: bool = True,
    ) -> ModelType:
        """Возвращает объект модели по его идентификатору."""
        query = (
            select(self.model)
            .where(self.model.id == instance_id)
        )

        async with self._db.get_session() as session:
            try:
                db_result = await session.execute(query)
                instance = db_result.scalar_one()
            except SQLAlchemyError as e:
                raise e  # type: ignore

            return self.serialize(instance) if is_serialize else instance

    async def get_list(self, is_serialize: bool = True, **kwargs: Any) -> ResultE[Iterable[ModelType]]:
        query = select(self.model)

        async with self._db.get_session() as session:
            try:
                db_result = await session.execute(query)
                instances = db_result.scalars()
            except SQLAlchemyError as e:
                raise e

            return self.serialize_many(instances) if is_serialize else instances

    @classmethod
    def serialize(
            cls,
            model_instance: ModelType,
            schema: Type[SchemaType] | None = None
    ) -> SchemaType:
        """Сериализует объект модели в объект переданной схемы."""
        schema = schema or cls.creation_schema
        return schema.model_validate(model_instance)

    @classmethod
    def serialize_many(
            cls,
            model_instances: Iterable[ModelType],
            schema: Type[SchemaType] | None = None
    ) -> Iterable[SchemaType]:
        """Сериализует объекты модели в объекты переданной схемы."""
        return [
            cls.serialize(model_instance=model_instance, schema=schema)
            for model_instance in model_instances
        ]
