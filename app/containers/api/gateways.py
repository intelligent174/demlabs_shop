from dependency_injector import (
    containers,
    providers,
)

from app.core.db.base import Database

__all__ = [
    'GatewayContainer',
]


class GatewayContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    db_demlabs_shop = providers.Singleton(
        Database,
        dsn_url=config.db.DSN,
    )
