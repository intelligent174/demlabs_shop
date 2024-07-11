from providers import (
    Provider,
    Scope,
    provide,
)

from app.auth.service import AuthService
from app.auth.utils.jwt import JWTUtility
from app.carts.repository import CartRepository
from app.carts.service import CartService
from app.categories.repository import CategoryRepository
from app.categories.service import CategoryService
from app.core.db.base import Database
from app.config import settings
from app.products.repository import ProductRepository
from app.products.service import ProductService
from app.registrations.service import RegistrationService
from app.users.repository import UserRepository
from app.users.service import UserService
from app.users.utils.password import PasswordUtility


class AdapterProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_demlabs_shop_db(self) -> Database:
        return Database(settings.db.DSN)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_category_repository(self, db_demlabs_shop: Database) -> CategoryRepository:
        return CategoryRepository(db_demlabs_shop)

    @provide
    async def get_cart_repository(self, db_demlabs_shop: Database) -> CartRepository:
        return CartRepository(db_demlabs_shop)

    @provide
    async def get_product_repository(self, db_demlabs_shop: Database) -> ProductRepository:
        return ProductRepository(db_demlabs_shop)

    @provide
    async def get_user_repository(self, db_demlabs_shop: Database) -> UserRepository:
        return UserRepository(db_demlabs_shop)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_auth_service(
            self,
            user_service: UserService,
            jwt_utility: JWTUtility,
    ) -> AuthService:
        return AuthService(
            user_service=user_service,
            jwt_utility=jwt_utility,
        )

    @provide
    async def get_category_service(self, repository: CategoryRepository) -> CategoryService:
        return CategoryService(repository=repository)

    @provide
    async def get_cart_service(self, repository: CartRepository) -> CartService:
        return CartService(repository=repository)

    @provide
    async def get_product_service(self, repository: ProductRepository) -> ProductService:
        return ProductService(repository=repository)

    @provide
    async def get_registration_service(self, user_service: UserService) -> RegistrationService:
        return RegistrationService(user_service=user_service)

    @provide
    async def get_user_service(
            self,
            repository: UserRepository,
            password_utility: PasswordUtility
    ) -> UserService:
        return UserService(
            repository=repository,
            password_utility=password_utility,
        )


class UtilityProvider(Provider):
    scope = Scope.REQUEST
    password_utility = provide(PasswordUtility)

    @provide
    async def get_jwt_utility(self) -> JWTUtility:
        return JWTUtility(
            private_secret_key=settings.jwt.PRIVATE_SECRET_KEY,
            public_secret_key=settings.jwt.PUBLIC_SECRET_KEY,
            access_token_expire_hours=settings.jwt.ACCESS_TOKEN_EXPIRE_HOURS,
            refresh_token_expire_hours=settings.jwt.REFRESH_TOKEN_EXPIRE_HOURS,
            algorithms=settings.jwt.ALGORITHMS,
        )
