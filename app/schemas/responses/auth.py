from pydantic import (
    SecretStr,
    BaseModel,
    field_serializer,
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


class AuthAccessTokenResponse(BaseModel):
    access_token: AuthTokenResponse
    token_type: str = 'Bearer'
