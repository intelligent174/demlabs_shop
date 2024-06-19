from uuid import UUID

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
    Failure,
)

from app.containers.api.services import ServiceContainer
from app.auth.utils.token_payload import CurrentToken
from app.products.schemas import (
    ProductCreateRequest,
    ProductCreateResponse,
    ProductListResponse,
)
from app.products.service import ProductService

name_prefix = 'product'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
)


@router.post(
    '/products/',
    name=f'{name_prefix}:creating_products',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
        request_data: ProductCreateRequest,
        service: ProductService = Depends(Provide[ServiceContainer.product_service]),
        token_payload=Depends(CurrentToken()),
) -> ProductCreateResponse:
    match await service.create_instance(data=request_data):
        case Success(product):
            return product
        case Failure(PRODUCT_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=PRODUCT_ALREADY_EXISTS)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/products/{product_id:uuid}/',
    name=f'{name_prefix}:getting_product',
    status_code=status.HTTP_200_OK,
)
@inject
async def get(
        product_id: UUID,
        service: ProductService = Depends(Provide[ServiceContainer.product_service]),
) -> ProductCreateResponse:
    match await service.get_by_id(product_id):
        case Success(product):
            return product
        case Failure(PRODUCT_NOT_FOUND):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/products/{category_id:uuid}',
    name=f'{name_prefix}:getting_products',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_list(
        category_id: UUID,
        service: ProductService = Depends(Provide[ServiceContainer.product_service]),
) -> ProductListResponse:
    match await service.get_list(category_id):
        case Success(products):
            return ProductListResponse(products=products)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
