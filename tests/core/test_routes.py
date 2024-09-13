import pytest

from tests.fixtures import *


class TestRoutes:


    @pytest.mark.anyio
    async def test_get_forecast5_async(self, async_client):
        response = await async_client.get("/forecast5", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.anyio
    async def test_get_forecast5_async_500(self, async_client):
        response = await async_client.get("/forecast5", params={"lat": 10.0})
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_get_interoperable_forecast5_async(self, async_client):
        response = await async_client.get("/interoperable/forecast5", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)