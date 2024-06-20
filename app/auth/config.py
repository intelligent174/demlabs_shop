from datetime import timedelta
from pathlib import Path

from pydantic import Field

from pydantic_settings import BaseSettings

__all__ = [
    'JWTConfigSchema',
]

QUANTITY_PATH_ANCESTORS = 2
BASE_DIR = Path(__file__).parents[QUANTITY_PATH_ANCESTORS]


class JWTConfigSchema(BaseSettings):
    PRIVATE_SECRET_KEY: Path = BASE_DIR / 'certificates' / 'jwt-private.pem'
    PUBLIC_SECRET_KEY: Path = BASE_DIR / 'certificates' / 'jwt-public.pem'
    ALGORITHMS: list[str] = Field(default=['RS256'])
    ACCESS_TOKEN_EXPIRE_HOURS: timedelta = Field(default=timedelta(hours=1))
    REFRESH_TOKEN_EXPIRE_HOURS: timedelta = Field(default=timedelta(days=16))
