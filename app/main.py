from fastapi import FastAPI

from app.containers.api.wires import (
    APP_CONTAINER_MODULES,
    wiring,
)
from app.auth.router import router as auth_router
from app.categories.router import router as router_category
from app.carts.router import router as cart_router
from app.products.router import router as router_product
from app.registrations.router import router as registration_router


def create_app() -> FastAPI:
    containers = wiring(modules=APP_CONTAINER_MODULES)
    app_container = containers['app_container']
    app = app_container.app_factory()

    # Router...
    app.include_router(registration_router)
    app.include_router(auth_router)
    app.include_router(router_category)
    app.include_router(router_product)
    app.include_router(cart_router)

    return app
