import pytest

from tests.fixtures import *


class TestRoutes:

    # Test succeessful call to API
    @pytest.mark.anyio
    async def get_weather_forecast5days(self, async_client):
        response = await async_client.get("/api/data/forecast5", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    # Test internal server error in API call
    @pytest.mark.anyio
    async def test_get_forecast5_500(self, async_client):
        response = await async_client.get("/api/data/forecast5", params={"lat": 10.0})
        assert response.status_code == 422

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld(self, async_client):
        response = await async_client.get("/api/linkeddata/forecast5", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

    # Test internal server error in API call
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_500(self, async_client):
        response = await async_client.get("/api/linkeddata/forecast5", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_weather(self, async_client):
        response = await async_client.get("/api/data/weather", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_thi(self, async_client):
        response = await async_client.get("/api/data/thi", params={"lat": 10.0, "lon": 20.0})
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

