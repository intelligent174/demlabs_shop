from typing import (
    Any,
    Generic,
    Iterable,
)
from uuid import UUID

from returns.maybe import Maybe
from returns.result import (
    Failure,
    Success,
    ResultE,
)
from sqlalchemy.exc import NoResultFound

from app.core.db.exceptions_types import CastViolationError
from app.core.repository.base import BaseAlchemyRepository
from app.core.repository.schemas_types import (
    BaseSchemaType,
    ModelType,
    CreateSchemaType,
)

__all__ = [
    'BaseCreateService',
]


class BaseService:
    _errors_map: dict

    def __init__(self, repository: BaseAlchemyRepository) -> None:
        self.repository = repository

    async def get_by_id(self, instance_id: UUID | str) -> Maybe[ModelType]:
        try:
            instance = await self.repository.get_by_id(instance_id)
            return Success(instance)
        except NoResultFound as e:
            error_message = self._errors_map.get(e.__class__.__name__, str(e))
            return Failure(error_message)
        except Exception as e:
            return Failure(str(e))  # type: ignore

    async def get_list(self, **kwargs: Any) -> ResultE[Iterable[ModelType]]:
        try:
            instances = await self.repository.get_list()
        except Exception as e:
            return Failure(str(e))
        return Success(instances)


class BaseCreateService(
    BaseService,
    Generic[
        ModelType,
        BaseSchemaType,
        CreateSchemaType,
    ],
):

    async def create_instance(
            self,
            data: CreateSchemaType,
            is_serialize: bool = True,
            exclude_fields: set[str] | None = None,
            exclude_none: bool = False,
            **kwargs: Any,
    ) -> BaseSchemaType | ModelType:
        kwargs.update(data.model_dump(
            exclude=exclude_fields,
            exclude_none=exclude_none,
        ))

        try:
            instance = await self.repository.create(
                data=kwargs,
                is_serialize=is_serialize,
            )
            return Success(instance)
        except CastViolationError as e:
            error_message = self._errors_map.get(e.constraint_name, str(e))
            return Failure(error_message)
        except Exception as e:
            return Failure(str(e))  # type: ignore
