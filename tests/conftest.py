import asyncio

from asyncio import AbstractEventLoop
from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient

import pytest

from returns.result import Success

from app.asgi import app as demlabs_app
from app.auth.schemas import AuthTokensPairResponse
from app.auth.utils.jwt import JWTUtility
from app.categories.models import Category
from app.config import (
    get_settings,
    Settings,
)
from app.core.db.base import Database
from app.core.db import Base
from tests.router_tests.test_categories.factories import CategoryFactory
from tests.router_tests.test_users.factories import UserFactory


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return demlabs_app


@pytest.fixture(scope='session')
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(autouse=True, scope='session')
async def db(settings: Settings) -> Database:
    db = Database(dsn_url=settings.db.DSN)

    async with db.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield db
    async with db.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request) -> AsyncGenerator[AbstractEventLoop, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def jwt_utility(settings: Settings) -> JWTUtility:
    return JWTUtility(
        private_secret_key=settings.jwt.PRIVATE_SECRET_KEY,
        public_secret_key=settings.jwt.PUBLIC_SECRET_KEY,
        access_token_expire_hours=settings.jwt.ACCESS_TOKEN_EXPIRE_HOURS,
        refresh_token_expire_hours=settings.jwt.REFRESH_TOKEN_EXPIRE_HOURS,
        algorithms=settings.jwt.ALGORITHMS,
    )


@pytest.fixture(scope='session')
async def token(jwt_utility: JWTUtility, user_factory: UserFactory) -> AuthTokensPairResponse:
    user = user_factory.build()

    match await jwt_utility.generate_tokens_pair(
        user=user,
        exclude_fields={'created_at', 'updated_at', 'date_of_birth'},
    ):
        case Success(tokens_pair):
            return tokens_pair


@pytest.fixture(scope='session')
async def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope='session')
async def url(app: FastAPI, request) -> str:
    name_prefix, action = request.param
    return app.url_path_for(f'{name_prefix}:{action}')


@pytest.fixture(scope='session')
async def category(db: Database) -> Category:
    async with db.get_session() as session:
        CategoryFactory.__async_session__ = session
        category_instance = await CategoryFactory.create_async()
    return category_instance
