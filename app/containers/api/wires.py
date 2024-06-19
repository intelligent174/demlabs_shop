from typing import Iterable

from dependency_injector.containers import DeclarativeContainer

from app.containers.api.app import AppContainer
from app.containers.api.gateways import GatewayContainer
from app.containers.api.repositories import RepositoryContainer
from app.containers.api.services import ServiceContainer
from app.core.configs import settings

__all__ = [
    'APP_CONTAINER_MODULES',
    'wiring',
]

APP_CONTAINER_MODULES = [
    'app.auth.router',
    'app.categories.router',
    'app.carts.router',
    'app.products.router',
    'app.registrations.router',
]


def wiring(modules: Iterable[str]) -> dict[str, DeclarativeContainer]:
    # Init...
    app_container = AppContainer()
    app_container.config.from_dict(settings.dict())
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
