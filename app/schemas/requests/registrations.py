from datetime import date

from pydantic import (
    SecretStr,
    BaseModel,
    EmailStr,
)

from app.schemas.fields.phone_number import PhoneNumber

__all__ = [
    'RegisterUserRequest',
]


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    patronymic_name: str
    date_of_birth: date
    email: EmailStr
    phone: PhoneNumber
    password: SecretStr
