from dependency_injector import containers, providers

from app.services.auth import AuthService
from app.services.carts import CartService
from app.services.categories import CategoryService
from app.services.product import ProductService
from app.services.registration import RegistrationService
from app.services.jwt import JWTService
from app.services.user import UserService
from app.services.password import PasswordService

__all__ = [
    'ServiceContainer',
]


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    repositories = providers.DependenciesContainer()

    password_service = providers.Factory(
        PasswordService,
    )
    user_service = providers.Factory(
        UserService,
        repository=repositories.user_repository,
        password_service=password_service,

    )
    jwt_service = providers.Factory(
        JWTService,
        private_secret_key=config.jwt.PRIVATE_SECRET_KEY,
        public_secret_key=config.jwt.PUBLIC_SECRET_KEY,
        access_token_expire_hours=config.jwt.ACCESS_TOKEN_EXPIRE_HOURS,
        refresh_token_expire_hours=config.jwt.REFRESH_TOKEN_EXPIRE_HOURS,
        algorithms=config.jwt.ALGORITHMS,

    )
    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        jwt_service=jwt_service,
    )
    registration_service = providers.Factory(
        RegistrationService,
        user_service=user_service,
    )
    product_service = providers.Factory(
        ProductService,
        repository=repositories.product_repository,
    )
    category_service = providers.Factory(
        CategoryService,
        repository=repositories.category_repository,
    )
    cart_service = providers.Factory(
        CartService,
        repository=repositories.cart_repository,
    )
