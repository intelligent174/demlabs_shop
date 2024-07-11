from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.categories.router import router as router_category
from app.carts.router import router as cart_router
from app.config import settings
from app.containers.api.providers import (
    AdapterProvider,
    ServiceProvider,
    RepositoryProvider,
    UtilityProvider,
)
from app.products.router import router as router_product
from app.registrations.router import router as registration_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app.TITLE,
        debug=settings.app.DEBUG,
        lifespan=lifespan,
    )
    # Router...
    app.include_router(registration_router)
    app.include_router(auth_router)
    app.include_router(router_category)
    app.include_router(router_product)
    app.include_router(cart_router)

    container = make_async_container(
        AdapterProvider(),
        ServiceProvider(),
        RepositoryProvider(),
        UtilityProvider(),
    )
    setup_dishka(container, app)

    return app
