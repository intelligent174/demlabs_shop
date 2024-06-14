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
from app.schemas.requests.registrations import RegisterUserRequest
from app.schemas.responses.users import UserCreateResponse
from app.services.registration import RegistrationService

name_prefix = 'registration'
router = APIRouter(tags=[name_prefix])


@router.post(
    '/register_user/',
    name=f'{name_prefix}:register_user',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_user(
        request_data: RegisterUserRequest,
        service: RegistrationService = Depends(Provide[ServiceContainer.registration_service]),
) -> UserCreateResponse:
    match await service.create_instance(data=request_data):
        case Success(user):
            return user
        case Failure(PHONE_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=PHONE_ALREADY_EXISTS)
        case Failure(EMAIL_ALREADY_EXISTS):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=EMAIL_ALREADY_EXISTS)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
