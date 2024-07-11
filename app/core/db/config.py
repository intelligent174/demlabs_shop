from typing import Any

from pydantic import (
    Field,
    PostgresDsn,
    field_validator,
)
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

__all__ = [
    'AsyncpgDbSettings',
]


class DbSettings(BaseSettings):
    HOST: str = Field(
        default=...,
        description='Database host. Without end slash',
    )
    PORT: int = Field(
        default=...,
        description='Database port',
    )

    NAME: str = Field(
        default=...,
        description='Database name',
    )
    USER: str
    PASSWORD: str

    POOL_MIN_SIZE: int = Field(default=10)
    POOL_MAX_SIZE: int = Field(default=10)

    RETRY_LIMIT: int = Field(default=10)
    RETRY_INTERVAL: int = Field(default=4)

    ECHO: bool = Field(default=True)
    SSL: bool = Field(default=False)
    USE_CONNECTION_FOR_REQUEST: bool = Field(default=True)

    DSN: str = Field(
        default='',
        description='Computed field',
    )

    model_config = SettingsConfigDict(
        env_file='.env.local',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='DB_',
    )

    # TODO: поискать другой способ формирования значения для свойства pydantic модели??
    @field_validator('DSN')
    def compute_dsn(
            cls,
            v: Any,
            values: ValidationInfo,
            **kwargs: object,
    ) -> str:
        return PostgresDsn.build(  # type: ignore
            scheme='postgresql',
            username=values.data['USER'],
            password=values.data['PASSWORD'],
            host=values.data['HOST'],
            port=values.data['PORT'],
            path=f"{values.data['NAME']}",
        )


class AsyncpgDbSettings(DbSettings):
    DSN: str = Field(
        default='',
        description='Computed field',
    )

    @field_validator('DSN')
    def compute_dsn(
            cls,
            v: Any,
            values: ValidationInfo,
            **kwargs: object,
    ) -> Any:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.data['USER'],
            password=values.data['PASSWORD'],
            host=values.data['HOST'],
            port=values.data['PORT'],
            path=f"{values.data['NAME']}",
        )
