from dependency_injector.wiring import (
    inject,
    Provide,
)
from fastapi import (
    HTTPException,
    Form,
    Depends,
    status,
)
from pydantic import SecretStr
from returns.result import (
    Success,
    Failure,
)

from app.users.models import User
from app.auth.exception_messages import INVALID_PASSWORD

from app.containers.api.services import ServiceContainer
from app.core.schemas.fields.phone_number import PhoneNumber
from app.users.service import UserService
from app.users.utils.password import PasswordService


class CurrentUser:
    @inject
    async def __call__(
            self,
            phone: PhoneNumber = Form(),
            password: SecretStr = Form(),
            user_service: UserService = Depends(Provide[ServiceContainer.user_service]),
            password_service: PasswordService = Depends(Provide[ServiceContainer.password_service]),
    ) -> User:
        match await user_service.get_user_by_phone(phone):
            case Success(user):
                if not password_service.validate_password(
                        password=password.get_secret_value(),
                        password_hash=user.password_hash,
                        password_salt=user.password_salt,
                ):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_PASSWORD)
                return user_service.serialize(user)
            case Failure(USER_NOT_FOUND):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=USER_NOT_FOUND)
