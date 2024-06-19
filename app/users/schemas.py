import datetime

from pydantic import EmailStr

from app.core.schemas.responses.common import (
    BaseResponseModel,
    ConfigDictMixin,
)

__all__ = [
    'UserCreateResponse',
]


class UserCreateResponse(BaseResponseModel, ConfigDictMixin):
    first_name: str
    last_name: str
    patronymic_name: str | None
    date_of_birth: datetime.datetime | None
    phone: str
    email: EmailStr | None
