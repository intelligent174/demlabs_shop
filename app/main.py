from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.categories.router import router as router_category
from app.carts.router import router as cart_router
from app.config import get_settings
from app.containers.api.providers import (
    AdapterProvider,
    CacheServiceProvider,
    ServiceProvider,
    RepositoryProvider,
    UtilityProvider,
    SettingProvider,
)
from app.products.router import router as router_product
from app.registrations.router import router as registration_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app.TITLE,
        debug=settings.app.DEBUG,
        lifespan=lifespan,
    )

    # Middlewares
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=settings.cors.ALLOW_ORIGINS,
        allow_credentials=settings.cors.ALLOW_CREDENTIALS,
        allow_methods=settings.cors.ALLOW_METHODS,
        allow_headers=settings.cors.ALLOW_HEADERS,
    )

    # Router...
    app.include_router(registration_router)
    app.include_router(auth_router)
    app.include_router(router_category)
    app.include_router(router_product)
    app.include_router(cart_router)

    return app


def create_production_app() -> FastAPI:
    app = create_app()
    container = make_async_container(
        AdapterProvider(),
        CacheServiceProvider(),
        ServiceProvider(),
        RepositoryProvider(),
        UtilityProvider(),
        SettingProvider(),
    )
    setup_dishka(container, app)

    return app
