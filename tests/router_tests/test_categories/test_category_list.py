from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.categories.router import name_prefix


class TestReadManyCategory:

    @pytest.mark.parametrize('url', [(name_prefix, 'list')], indirect=True)
    async def test_when_valid_data_passed_then_category_read(
            self,
            url: str,
            async_client: AsyncClient,
    ) -> None:
        response = await async_client.get(url=url)
        response.raise_for_status()

        assert response.status_code == HTTPStatus.OK, response.json()
