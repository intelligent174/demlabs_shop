from functools import cached_property

from pydantic import (
    BaseModel,
    SecretStr,
    field_serializer,
    computed_field,
)

__all__ = [
    'AuthTokenResponse',
    'AuthTokensPairResponse',
    'AuthAccessTokenResponse',
]


class AuthTokenResponse(BaseModel):
    token: SecretStr

    @field_serializer('token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()


class AuthTokensPairResponse(BaseModel):
    access_token: AuthTokenResponse
    refresh_token: AuthTokenResponse
    token_type: str = 'Bearer'

    @computed_field(repr=False)
    @cached_property
    def token(self) -> str:
        return self.access_token.token.get_secret_value()


class AuthAccessTokenResponse(BaseModel):
    access_token: AuthTokenResponse
    token_type: str = 'Bearer'
