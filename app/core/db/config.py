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


class AsyncpgDbSettings(BaseSettings):
    HOST: str = Field(
        default=...,
        description='Database host. Without end slash',
    )
    PORT: int = Field(
        default=...,
        description='Database port',
    )
    DB: str = Field(
        default=...,
        description='Database name',
    )
    USER: str
    PASSWORD: str

    DSN: str = Field(
        default='',
        description='Computed field',
    )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='POSTGRES_',
        secrets_dir='/run/secrets',
    )

    # TODO: поискать другой способ формирования значения для свойства pydantic модели??
    @field_validator('DSN')
    def compute_dsn(
            cls,
            v: str,
            values: ValidationInfo,
            **kwargs: object,
    ) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.data['USER'],
            password=values.data['PASSWORD'],
            host=values.data['HOST'],
            port=values.data['PORT'],
            path=f'{values.data['DB']}',
        ).unicode_string()
