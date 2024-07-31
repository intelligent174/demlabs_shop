from typing import Sequence

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

__all__ = [
    'CORSConfigSettings',
]


class CORSConfigSettings(BaseSettings):
    ALLOW_ORIGINS: Sequence[str] = Field(default=('*',))
    ALLOW_CREDENTIALS: bool = Field(default=False)
    ALLOW_METHODS: Sequence[str] = Field(default=('*',))
    ALLOW_HEADERS: Sequence[str] = Field(default=('*',))

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='CORS_',
    )
