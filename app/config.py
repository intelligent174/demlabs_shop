from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.auth.config import JWTSettings
from app.core.cache.config import RedisSettings
from app.core.db.config import AsyncpgDbSettings

__all__ = [
    'settings',
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
        env_file='.env.local',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='APP_',
    )


# TODO: переделать под Pydantic 2.
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: AsyncpgDbSettings = AsyncpgDbSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
