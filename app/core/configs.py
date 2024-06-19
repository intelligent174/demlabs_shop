from datetime import timedelta
from pathlib import Path
from typing import Any

from pydantic import (
    Field,
    PostgresDsn,
    field_validator,
)
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

__all__ = [
    'settings',
]

QUANTITY_PATH_ANCESTORS = 2
BASE_DIR = Path(__file__).parents[QUANTITY_PATH_ANCESTORS]


class AppConfigSchema(BaseSettings):
    TITLE: str = Field(
        default='Demlabs Shop Service',
        description='The Demlabs store is opening soon',
    )
    DEBUG: bool = Field(default=True)

    class Config:
        env_prefix = 'APP_'
        case_sensitive = True


class DbConfigSchema(BaseSettings):
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

    class Config:
        env_prefix = 'DB_'
        case_sensitive = True

    @field_validator('DSN')
    def compute_dsn(
            cls,
            v: Any,
            values: Any,
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


class JWTConfigSchema(BaseSettings):
    PRIVATE_SECRET_KEY: Path = BASE_DIR / 'certificates' / 'jwt-private.pem'
    PUBLIC_SECRET_KEY: Path = BASE_DIR / 'certificates' / 'jwt-public.pem'
    ALGORITHMS: list[str] = Field(default=['RS256'])
    ACCESS_TOKEN_EXPIRE_HOURS: timedelta = Field(default=timedelta(hours=1))
    REFRESH_TOKEN_EXPIRE_HOURS: timedelta = Field(default=timedelta(days=16))

    class Config:
        env_prefix = 'JWT_'
        case_sensitive = True


class AsyncpgDbConfigSchema(DbConfigSchema):
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


class ConfigSchema(BaseSettings):
    app: AppConfigSchema = AppConfigSchema()
    db: AsyncpgDbConfigSchema = AsyncpgDbConfigSchema()
    jwt: JWTConfigSchema = JWTConfigSchema()


settings = ConfigSchema()
