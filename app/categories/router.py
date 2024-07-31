from typing import List

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
    route_class=DishkaRoute,
)


@router.post(
    '/categories/',
    name=f'{name_prefix}:create',
    response_model=CategoryCreateResponse,
)
async def create(
        request_data: CategoryCreateRequest,
        service: FromDishka[CategoryService],
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
    name=f'{name_prefix}:list',
    response_model=List[CategoryCreateResponse],
)
async def get_list(
        service: FromDishka[CategoryService],
) -> CustomJSONResponse:
    match await service.get_list():
        case Success(categories):
            return CustomJSONResponse(categories, status_code=status.HTTP_200_OK)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
