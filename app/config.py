from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.auth.config import JWTSettings
from app.core.cache.config import RedisSettings
from app.core.db.config import AsyncpgDbSettings
from app.core.middlewares.config import CORSConfigSettings

__all__ = [
    'get_settings',
    'Settings',
]

QUANTITY_PATH_ANCESTORS = 2
BASE_DIR = Path(__file__).parents[QUANTITY_PATH_ANCESTORS]


class AppSettings(BaseSettings):
    TITLE: str = Field(
        default='Demlabs Shop Service',
        description='The Demlabs store is opening soon',
    )
    DEBUG: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='APP_',
    )


# TODO: переделать под Pydantic 2.
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    cors: CORSConfigSettings = CORSConfigSettings()
    db: AsyncpgDbSettings = AsyncpgDbSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
