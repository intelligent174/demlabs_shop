from http import HTTPStatus

import pytest

from orjson.orjson import loads
from httpx import AsyncClient

from app.auth.schemas import AuthTokensPairResponse
from app.categories.models import Category
from app.categories.router import name_prefix
from tests.router_tests.test_categories.factories import CategoryCreateRequestFactory


class TestCreateCategory:

    @pytest.mark.parametrize('url', [(name_prefix, 'create')], indirect=True)
    async def test_when_valid_data_passed_then_category_created(
            self,
            url: str,
            async_client: AsyncClient,
            category_create_request_factory: CategoryCreateRequestFactory,
            token: AuthTokensPairResponse,
    ) -> None:
        body = category_create_request_factory.build()

        response = await async_client.post(
            url=url,
            json=loads(body.model_dump_json()),
            headers={'Authorization': f'{token.token_type} {token.token}'},
        )
        response.raise_for_status()
        response_data = response.json()

        assert response_data['title'] == body.title

    @pytest.mark.parametrize('url', [(name_prefix, 'create')], indirect=True)
    async def test_when_category_already_exists_then_conflict(
            self,
            async_client: AsyncClient,
            category_create_request_factory: CategoryCreateRequestFactory,
            category: Category,
            token: AuthTokensPairResponse,
            url: str,
    ) -> None:
        body = category_create_request_factory.build(title=category.title)

        response = await async_client.post(
            url=url,
            json=loads(body.model_dump_json()),
            headers={'Authorization': f'{token.token_type} {token.token}'},
        )

        assert response.status_code == HTTPStatus.CONFLICT, response.json()
