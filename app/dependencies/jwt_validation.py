from dependency_injector.wiring import (
    inject,
    Provide,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from returns.result import (
    Success,
    Failure,
)

from app.containers.api.services import ServiceContainer
from app.services.jwt import JWTService

http_bearer = HTTPBearer()


class CurrentToken:
    def __init__(self, token_type: str = 'access'):
        self.token_type = token_type

    @inject
    async def __call__(
            self,
            token: HTTPAuthorizationCredentials = Depends(http_bearer),
            jwt_service: JWTService = Depends(Provide[ServiceContainer.jwt_service]),
    ):
        if self.token_type == 'access':
            match await jwt_service.decode_token(token=token.credentials, token_type=self.token_type):
                case Success(payload):
                    return payload
                case Failure(INVALID_TOKEN):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN)
                case Failure(INVALID_TOKEN_TYPE):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN_TYPE)
                case _:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        elif self.token_type == 'refresh':
            match await jwt_service.decode_token(token=token.credentials, token_type=self.token_type):
                case Success(payload):
                    return payload.get('sub')
                case Failure(INVALID_TOKEN):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN)
                case Failure(INVALID_TOKEN_TYPE):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN_TYPE)
                case _:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
