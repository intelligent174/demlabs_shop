from fastapi import (
    APIRouter,
    FastAPI,
)

from app.containers.api.wires import (
    APP_CONTAINER_MODULES,
    wiring,
)
from app.views import root_router


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(root_router)
    return router


def create_app() -> FastAPI:
    containers = wiring(modules=APP_CONTAINER_MODULES)
    app_container = containers['app_container']
    app = app_container.app_factory()

    # Router...
    router = get_router()
    app.include_router(router)

    return app
