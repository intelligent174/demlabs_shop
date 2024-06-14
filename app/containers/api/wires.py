from typing import Iterable

from dependency_injector.containers import DeclarativeContainer

from app.containers.api.app import AppContainer
from app.containers.api.gateways import GatewayContainer
from app.containers.api.repositories import RepositoryContainer
from app.containers.api.services import ServiceContainer
from app.core.configs import get_config

__all__ = [
    'APP_CONTAINER_MODULES',
    'wiring',
]

APP_CONTAINER_MODULES = [
    'app.views.auth',
    'app.views.carts',
    'app.views.categories',
    'app.views.products',
    'app.views.registrations',
]


def wiring(modules: Iterable[str]) -> dict[str, DeclarativeContainer]:
    config = get_config()

    # Init...
    app_container = AppContainer()
    app_container.config.from_dict(config.model_dump())
    app_container.wire(modules=modules)

    gateways_container = GatewayContainer(
        config=app_container.config,
    )
    repositories_container = RepositoryContainer(
        config=app_container.config,
        gateways=gateways_container,
    )
    services_container = ServiceContainer(
        config=app_container.config,
        repositories=repositories_container,
    )

    # Wiring...
    gateways_container.wire(modules=modules)
    repositories_container.wire(modules=modules)
    services_container.wire(modules=modules)

    return {
        'app_container': app_container,
        'repositories_container': repositories_container,
        'gateways_container': gateways_container,
        'service_container': services_container,
    }
