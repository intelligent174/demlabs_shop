from typing import List

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
)
from app.categories.service import CategoryService
from app.utils.schemas import CustomJSONResponse

name_prefix = 'category'
router = APIRouter(
    prefix=f'/{name_prefix}',
    tags=[name_prefix],
)


@router.post(
    '/categories/',
    name=f'{name_prefix}:creating_categories',
    response_model=CategoryCreateResponse,
)
@inject
async def create(
        request_data: CategoryCreateRequest,
        service: CategoryService = Depends(Provide[ServiceContainer.category_service]),
        token_payload=Depends(CurrentToken()),
) -> CustomJSONResponse:
    match await service.create_instance(data=request_data):
        case Success(category):
            return CustomJSONResponse(category, status_code=status.HTTP_201_CREATED)
        case Failure(CATEGORY_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=CATEGORY_ALREADY_EXISTS)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/categories/',
    name=f'{name_prefix}:getting_categories',
    response_model=List[CategoryCreateResponse],
)
@inject
async def get(
        service: CategoryService = Depends(Provide[ServiceContainer.category_service]),
) -> CustomJSONResponse:
    match await service.get_list():
        case Success(categories):
            return CustomJSONResponse(categories, status_code=status.HTTP_200_OK)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
