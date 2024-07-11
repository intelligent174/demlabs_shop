from returns.result import (
    Failure,
    Success,
    Result,
)

from app.users.schemas import UserCreateResponse
from app.auth.utils.jwt import JWTUtility
from app.users.service import UserService

__all__ = [
    'AuthService',
]


class AuthService:

    def __init__(
            self,
            user_service: UserService,
            jwt_utility: JWTUtility,
    ):
        self.user_service = user_service
        self.jwt_utility = jwt_utility

    async def login_phone(self, user: UserCreateResponse):
        match await self.jwt_utility.generate_tokens_pair(
            user=user,
            exclude_fields={'date_of_birth', 'created_at', 'updated_at'},
        ):
            case Success(tokens_pair):
                return Success(tokens_pair)

    async def refresh_auth(self, user_id: str) -> Result[str, str]:
        match await self.user_service.get_by_id(user_id):
            case Success(user):
                access_token = await self.jwt_utility.generate_access_token(
                    user=user,
                    exclude_fields={'date_of_birth', 'created_at', 'updated_at'},
                )
                return Success(access_token)
            case Failure(USER_NOT_FOUND):
                return Failure(USER_NOT_FOUND)
