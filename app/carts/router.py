from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from returns.result import (
    Success,
)

from app.containers.api.services import ServiceContainer
from app.auth.utils.token_payload import CurrentToken
from app.carts.schemas import CartCreateRequest
from app.carts.schemas import CartCreateResponse
from app.carts.service import CartService
from app.utils.schemas import CustomJSONResponse

name_prefix = 'cart'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
)


@router.post(
    '/carts/',
    name=f'{name_prefix}:creating_cart',
    response_model=CartCreateResponse,
)
@inject
async def create(
        request_data: CartCreateRequest,
        service: CartService = Depends(Provide[ServiceContainer.cart_service]),
        token_payload=Depends(CurrentToken()),
) -> CustomJSONResponse:
    match await service.create_instance(data=request_data, user_id=token_payload.get('sub')):
        case Success(cart):
            return CustomJSONResponse(cart, status_code=status.HTTP_201_CREATED)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
