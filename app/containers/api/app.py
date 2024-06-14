from dependency_injector import (
    containers,
    providers,
)
from fastapi import FastAPI

__all__ = [
    'AppContainer',
]


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    app_factory = providers.Factory(
        FastAPI,
        title=config.app.TITLE,
        debug=config.app.DEBUG,
    )
