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
from app.categories.schemas import (
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryListResponse,
)
from app.categories.service import CategoryService

name_prefix = 'category'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
)


@router.post(
    '/categories/',
    name=f'{name_prefix}:creating_categories',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
        request_data: CategoryCreateRequest,
        service: CategoryService = Depends(Provide[ServiceContainer.category_service]),
        token_payload=Depends(CurrentToken()),
) -> CategoryCreateResponse:
    match await service.create_instance(data=request_data):
        case Success(category):
            return category
        case Failure(CATEGORY_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=CATEGORY_ALREADY_EXISTS)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/categories/',
    name=f'{name_prefix}:getting_categories',
    status_code=status.HTTP_200_OK,
)
@inject
async def get(
        service: CategoryService = Depends(Provide[ServiceContainer.category_service]),
) -> CategoryListResponse:
    match await service.get_list():
        case Success(categories):
            return CategoryListResponse(categories=categories)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
