from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, HTTPException
from returns.result import Success, Failure

from app.auth.utils.token_payload import CurrentToken
from app.auth.utils.user_authentication import CurrentUser
from app.auth.schemas import (
    AuthTokensPairResponse,
    AuthAccessTokenResponse,
)
from app.users.schemas import UserCreateResponse
from app.auth.service import AuthService
from app.utils.schemas import CustomJSONResponse

name_prefix = 'auth'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
    route_class=DishkaRoute,
)


@router.post(
    '/login/',
    name=f'{name_prefix}:phone_login',
    response_model=AuthTokensPairResponse,
)
async def login(
        service: FromDishka[AuthService],
        user: UserCreateResponse = Depends(CurrentUser()),
) -> CustomJSONResponse:
    match await service.login_phone(user=user):
        case Success(tokens_pair):
            return CustomJSONResponse(tokens_pair, status_code=status.HTTP_200_OK)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    '/refresh/',
    name=f'{name_prefix}:refresh',
    response_model=AuthAccessTokenResponse,
)
async def refresh_auth(
        service: FromDishka[AuthService],
        user_id=Depends(CurrentToken(token_type='refresh')),
) -> CustomJSONResponse:
    match await service.refresh_auth(user_id=user_id):
        case Success(access_token):
            return CustomJSONResponse(access_token, status_code=status.HTTP_200_OK)
        case Failure(USER_NOT_FOUND):
            raise HTTPException(status_code=status.NOT_FOUND, detail=USER_NOT_FOUND)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
