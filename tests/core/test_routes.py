import pytest

from tests.fixtures import *


class TestRoutes:

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_200(self, test_jwt_token, async_client):
        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/forecast5", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    # Test missing query param
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_422(self, test_jwt_token, async_client):
        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/forecast5", params={"lat": 10.0}, headers=headers)
        assert response.status_code == 422

    # Test internal server error
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_500(self, test_jwt_token, async_client, app):
        mock = AsyncMock(side_effect=ValueError)
        app.weather_app.get_weather_forecast5days = mock

        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/forecast5", params={"lat": 10.0, "lon": 33.42}, headers=headers)
        assert response.status_code == 500

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_200(self, test_jwt_token, async_client):
        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/linkeddata/forecast5", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    # Test internal server error in API call
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_500(self, test_jwt_token, async_client, app):
        mock = AsyncMock(side_effect=ValueError)
        app.weather_app.get_weather_forecast5days_ld = mock

        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/linkeddata/forecast5", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 500

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_weather_200(self, test_jwt_token, async_client):
        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/weather", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

    # Test internal server error in API call
    @pytest.mark.anyio
    async def test_get_weather_500(self, test_jwt_token, async_client, app):
        mock = AsyncMock(side_effect=ValueError)
        app.weather_app.get_weather = mock

        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/weather", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 500

    # Test succeessful call to API
    @pytest.mark.anyio
    async def test_get_thi_200(self, test_jwt_token, async_client):
        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/thi", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 200
        # assert isinstance(response.json(), dict)

    # Test internal server error in API call
    @pytest.mark.anyio
    async def test_get_thi_500(self, test_jwt_token, async_client, app):
        mock = AsyncMock(side_effect=ValueError)
        app.weather_app.get_thi = mock

        headers = {"Authorization": f"Bearer {test_jwt_token}"}
        response = await async_client.get("/api/data/thi", params={"lat": 10.0, "lon": 20.0}, headers=headers)
        assert response.status_code == 500