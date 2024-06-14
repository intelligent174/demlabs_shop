from typing import Any

from returns.result import (
    Success,
    Failure,
    Result,
)

from app.core.service.base import BaseCreateService
from app.schemas.requests.registrations import RegisterUserRequest
from app.schemas.responses.users import UserCreateResponse
from app.services.user import UserService

__all__ = [
    'RegistrationService',
]


class RegistrationService(BaseCreateService):

    def __init__(self, user_service: UserService):
        super().__init__()
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
