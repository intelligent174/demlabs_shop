from typing import Any

from returns.result import (
    Success,
    Failure,
    Result,
)

from app.core.repository.base import BaseAlchemyRepository
from app.core.service.base import BaseCreateService
from app.registrations.schemas import RegisterUserRequest
from app.users.schemas import UserCreateResponse
from app.users.service import UserService

__all__ = [
    'RegistrationService',
]


class RegistrationService(BaseCreateService):

    def __init__(
            self,
            user_service: UserService,
            repository: BaseAlchemyRepository = None,
    ) -> None:
        super().__init__(repository=repository)
        self.user_service = user_service

    async def create_instance(
            self,
            data: RegisterUserRequest,
            is_serialize: bool = True,
            exclude_fields: set[str] | None = None,
            exclude_none: bool = False,
            **kwargs: Any,
    ) -> Result[UserCreateResponse, str]:
        match await self.user_service.create_instance(
            data=data,
            exclude_fields={'password'},
        ):
            case Success(user):
                return Success(user)
            case Failure(PHONE_ALREADY_EXISTS):
                return Failure(PHONE_ALREADY_EXISTS)
            case Failure(EMAIL_ALREADY_EXISTS):
                return Failure(EMAIL_ALREADY_EXISTS)
