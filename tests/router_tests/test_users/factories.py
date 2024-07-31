from typing import (
    Type,
    Any,
)

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from app.core.schemas.fields.phone_number import PhoneNumber
from app.users.schemas import UserCreateResponse


@register_fixture(scope='session')
class UserFactory(ModelFactory[UserCreateResponse]):

    @classmethod
    def get_provider_map(cls) -> dict[Type, Any]:
        providers_map = super().get_provider_map()

        return {
            PhoneNumber: lambda: PhoneNumber('+79999999999'),
            **providers_map,
        }
