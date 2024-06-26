from typing import Any

from returns.maybe import Maybe
from returns.result import (
    Failure,
    Success,
)
from sqlalchemy.exc import NoResultFound

from app.core.db.exceptions_types import CastViolationError
from app.core.repository.schemas_types import (
    BaseSchemaType,
    ModelType,
)
from app.core.service.base import BaseCreateService
from app.users.models import User
from app.users.repository import UserRepository
from app.users.exception_messages import (
    EMAIL_ALREADY_EXISTS,
    PHONE_ALREADY_EXISTS,
    USER_NOT_FOUND,
)
from app.core.schemas.fields.phone_number import PhoneNumber
from app.registrations.schemas import RegisterUserRequest
from app.users.schemas import UserCreateResponse
from app.users.utils.password import PasswordService

__all__ = [
    'UserService',
]


class UserService(BaseCreateService):
    _errors_map = {
        'user_phone_key': PHONE_ALREADY_EXISTS,
        'user_email_key': EMAIL_ALREADY_EXISTS,
        'NoResultFound': USER_NOT_FOUND,
    }

    def __init__(self, repository: UserRepository, password_service: PasswordService) -> None:
        super().__init__(repository=repository)
        self.password_service = password_service

    async def get_user_by_phone(self, phone: PhoneNumber) -> Maybe[User]:
        try:
            user = await self.repository.get_user_by_phone(
                phone=phone,
                is_serialize=False,
            )
            return Success(user)
        except NoResultFound:
            return Failure(USER_NOT_FOUND)

    async def create_instance(
            self,
            data: RegisterUserRequest,
            is_serialize: bool = True,
            exclude_fields: set[str] | None = None,
            exclude_none: bool = False,
            **kwargs: Any,
    ) -> UserCreateResponse:
        kwargs.update(data.model_dump(
            exclude=exclude_fields,
            exclude_none=exclude_none,
        ))

        password_hash, password_salt = self.password_service.generate_hash(
            password=data.password.get_secret_value()
        )

        try:
            user = await self.repository.create(
                data=kwargs,
                password_hash=password_hash,
                password_salt=password_salt,
            )
            return Success(user)
        except CastViolationError as e:
            error_message = self._errors_map.get(e.constraint_name, str(e))
            return Failure(error_message)
        except Exception as e:
            return Failure(str(e))

    def serialize(self, model_instance: ModelType) -> BaseSchemaType:
        """Сериализует объекты модели в объекты схемы указанной в репозитории UserRepository"""
        return self.repository.serialize(model_instance)
