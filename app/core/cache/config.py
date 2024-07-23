from pydantic import (
    Field,
    field_validator,
    RedisDsn,
)
from pydantic_core.core_schema import ValidationInfo

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

__all__ = [
    'RedisSettings',
]


class RedisSettings(BaseSettings):
    HOST: str = Field(default='localhost')
    PORT: int = Field(default=6379)
    PASSWORD: str = Field(default='')

    DB: int = Field(default=0)

    DSN: str = Field(
        default='redis://localhost:6379//1',
        description='Computed field',
    )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='REDIS_',
        secrets_dir='/run/secrets',
    )

    @field_validator('DSN')
    def compute_dsn(
            cls,
            v: str,
            values: ValidationInfo,
            **kwargs: object,
    ) -> RedisDsn:
        return RedisDsn.build(  # type: ignore
            scheme='redis',
            password=values.data['PASSWORD'],
            host=values.data['HOST'],
            port=values.data['PORT'],
            path=f'/{values.data['DB']}',
        )
