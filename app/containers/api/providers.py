from dishka import (
    Provider,
    Scope,
    provide,
)
from redis import asyncio as redis
from redis.asyncio import Redis

from app.auth.service import AuthService
from app.auth.utils.jwt import JWTUtility
from app.carts.repository import CartRepository
from app.carts.service import CartService
from app.categories.repository import CategoryRepository
from app.categories.service import CategoryService
from app.core.db.base import Database
from app.config import (
    get_settings,
    Settings,
)
from app.products.cache import ProductRedisService
from app.products.repository import ProductRepository
from app.products.service import ProductService
from app.registrations.service import RegistrationService
from app.users.repository import UserRepository
from app.users.service import UserService
from app.users.utils.password import PasswordUtility


class SettingProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_settings(self) -> Settings:
        return get_settings()


class AdapterProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_demlabs_shop_db(self, settings: Settings) -> Database:
        return Database(settings.db.DSN)

    @provide
    async def get_redis_db(self, settings: Settings) -> Redis:
        return redis.from_url(str(settings.redis.DSN))


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
    async def get_product_service(
            self,
            repository: ProductRepository,
            cache: ProductRedisService,
    ) -> ProductService:
        return ProductService(repository=repository, cache=cache)

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


class CacheServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_product_redis_service(self, redis_pool: Redis) -> ProductRedisService:
        return ProductRedisService(redis_pool=redis_pool)


class UtilityProvider(Provider):
    scope = Scope.REQUEST
    password_utility = provide(PasswordUtility)

    @provide
    async def get_jwt_utility(self, settings: Settings) -> JWTUtility:
        return JWTUtility(
            private_secret_key=settings.jwt.PRIVATE_SECRET_KEY,
            public_secret_key=settings.jwt.PUBLIC_SECRET_KEY,
            access_token_expire_hours=settings.jwt.ACCESS_TOKEN_EXPIRE_HOURS,
            refresh_token_expire_hours=settings.jwt.REFRESH_TOKEN_EXPIRE_HOURS,
            algorithms=settings.jwt.ALGORITHMS,
        )
