from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.auth.config import JWTConfigSchema
from app.core.db.config import AsyncpgDbConfigSchema

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

    model_config = SettingsConfigDict(
        env_file='.env.local',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='APP_',
    )


class ConfigSchema(BaseSettings):
    app: AppConfigSchema = AppConfigSchema()
    db: AsyncpgDbConfigSchema = AsyncpgDbConfigSchema()
    jwt: JWTConfigSchema = JWTConfigSchema()


settings = ConfigSchema()
