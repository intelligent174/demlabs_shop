from fastapi import Form
from pydantic import BaseModel, SecretStr

from app.schemas.fields.phone_number import PhoneNumber

__all__ = [
    'PhoneLoginRequest',
]


class PhoneLoginRequest(BaseModel):
    phone: PhoneNumber = Form(),
    password: SecretStr = Form(),
