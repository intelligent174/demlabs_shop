import jwt

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Any

from jwt import InvalidTokenError
from returns.result import (
    Failure,
    Success,
    Result,
)

from app.auth.exception_messages import (
    INVALID_TOKEN,
    INVALID_TOKEN_TYPE,
)
from app.auth.schemas import (
    AuthTokenResponse,
    AuthTokensPairResponse,
    AuthAccessTokenResponse,
)
from app.users.schemas import UserCreateResponse


class JWTUtility:
    FIRST_ALGORITHM = 0
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'

    def __init__(
            self,
            public_secret_key: str,
            private_secret_key: str,
            algorithms: list[str],
            access_token_expire_hours: timedelta,
            refresh_token_expire_hours: timedelta,
    ):
        self.public_secret_key = public_secret_key
        self.private_secret_key = private_secret_key
        self.access_token_expire_hours = access_token_expire_hours
        self.refresh_token_expire_hours = refresh_token_expire_hours
        self.algorithms = algorithms

    async def generate_tokens_pair(
            self,
            user: UserCreateResponse,
            exclude_fields: set[str] | None = None,
    ) -> Success[AuthTokensPairResponse]:
        user_data = user.model_dump(exclude=exclude_fields)
        current_time = datetime.now(timezone.utc)

        access_token = await self._generate_access_token(
            token_data=user_data,
            expire=self.access_token_expire_hours,
            current_time=current_time,
        )
        refresh_token = await self._generate_refresh_token(
            token_data=user_data,
            expire=self.refresh_token_expire_hours,
            current_time=current_time,
        )
        tokens_pair = AuthTokensPairResponse(
            access_token=AuthTokenResponse(token=access_token),
            refresh_token=AuthTokenResponse(token=refresh_token),
        )

        return Success(tokens_pair)

    async def generate_access_token(
            self,
            user: UserCreateResponse,
            exclude_fields: set[str] | None = None,
    ) -> AuthAccessTokenResponse:
        user_data = user.model_dump(exclude=exclude_fields)
        current_time = datetime.now(timezone.utc)

        access_token = await self._generate_access_token(
            token_data=user_data,
            expire=self.access_token_expire_hours,
            current_time=current_time,
        )

        return AuthAccessTokenResponse(
            access_token=AuthTokenResponse(token=access_token)
        )

    async def decode_token(
            self,
            token: str | bytes,
            token_type: str,
    ) -> Result[str, str]:
        match await self._decode_token(token=token):
            case Success(payload):
                current_token_type = payload.get('token_type')

                if token_type != current_token_type:
                    return Failure(INVALID_TOKEN_TYPE)

                return Success(payload)
            case Failure(INVALID_TOKEN):
                return Failure(INVALID_TOKEN)

    async def _generate_access_token(
            self,
            expire: timedelta,
            current_time: datetime,
            token_data: dict[str, Any] = None,
    ) -> str:
        to_encode = token_data.copy()
        to_encode['sub'] = str(to_encode.pop('id'))
        to_encode['token_type'] = self.ACCESS_TOKEN_TYPE
        expire = current_time + expire
        to_encode.update(exp=expire, iat=current_time)

        return await self._encode_jwt(to_encode=to_encode)

    async def _generate_refresh_token(
            self,
            expire: timedelta,
            current_time: datetime,
            token_data: dict[str, Any] = None,
    ) -> str:
        to_encode = {
            'sub': str(token_data.get('id')),
            'token_type': self.REFRESH_TOKEN_TYPE,
            'exp': current_time + expire,
            'iat': current_time,
        }

        return await self._encode_jwt(to_encode=to_encode)

    async def _encode_jwt(self, to_encode: dict[str, Any]) -> str:
        return jwt.encode(
            to_encode,
            self.private_secret_key.read_text(),  # type: ignore
            algorithm=self.algorithms[self.FIRST_ALGORITHM],
        )

    async def _decode_token(self, token: str | bytes) -> Result[str, str]:
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self.public_secret_key.read_text(),  # type: ignore
                algorithms=self.algorithms,
            )
            return Success(decoded)
        except InvalidTokenError:
            return Failure(INVALID_TOKEN)
