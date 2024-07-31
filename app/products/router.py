from typing import List
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from returns.result import (
    Success,
    Failure,
)

from app.auth.utils.token_payload import CurrentToken
from app.products.schemas import (
    ProductCreateRequest,
    ProductCreateResponse,
    BaseProductResponse,
)
from app.products.service import ProductService
from app.utils.schemas import CustomJSONResponse

name_prefix = 'product'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
    route_class=DishkaRoute,
)


@router.post(
    '/products/',
    name=f'{name_prefix}:create',
    response_model=ProductCreateResponse,
)
async def create(
        request_data: ProductCreateRequest,
        service: FromDishka[ProductService],
        token_payload=Depends(CurrentToken()),
) -> CustomJSONResponse:
    match await service.create_instance(data=request_data):
        case Success(product):
            return CustomJSONResponse(product, status_code=status.HTTP_201_CREATED)
        case Failure(PRODUCT_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=PRODUCT_ALREADY_EXISTS)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/products/{product_id:uuid}/',
    name=f'{name_prefix}:read',
    response_model=ProductCreateResponse,
)
async def get(
        product_id: UUID,
        service: FromDishka[ProductService],
) -> CustomJSONResponse:
    match await service.get_by_id(product_id):
        case Success(product):
            return CustomJSONResponse(product, status_code=status.HTTP_200_OK)
        case Failure(PRODUCT_NOT_FOUND):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/products/{category_id:uuid}',
    name=f'{name_prefix}:list',
    response_model=List[BaseProductResponse],
)
async def get_list(
        category_id: UUID,
        service: FromDishka[ProductService],
) -> CustomJSONResponse:
    match await service.get_list(category_id):
        case Success(products):
            return CustomJSONResponse(products, status_code=status.HTTP_200_OK)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
