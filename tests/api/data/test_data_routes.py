import pytest
from unittest.mock import AsyncMock
import uuid
from fastapi import HTTPException


BASE_PARAMS = {"lat": 40.7128, "lon": -74.0060}

class TestDataRoutes:

    @pytest.fixture
    def mock_weather_data_out(self):
        return {
            "id": "bad6cd67-638f-42d8-82b8-d4d191174dd6",
            "spatial_entity": {
                "location": {
                    "type": "Point",
                    "coordinates": [40.7128, -74.0060]
                }
            },
            "data": {
                "weather": [{"description": "clear sky"}],
                "main": {"temp": 25.5, "humidity": 60, "pressure": 1013},
                "wind": {"speed": 5.2},
                "dt": 1640995200
            }
    }
    @pytest.fixture
    def mock_thi_data_out(self, mock_location):
        return {
            "id": str(uuid.uuid4()),
            "spatial_entity": {"location": mock_location},
            "thi": 72.5
        }
    @pytest.fixture
    def mock_jsonld_response(self):
        return {
            "@context": [
                "https://www.w3.org/ns/sosa/",
                {"@vocab": "https://example.org/"}
            ],
            "@graph": [
                {
                    "@id": "urn:example:location:1",
                    "@type": ["FeatureOfInterest", "Point"],
                    "lon": -74.0060,
                    "lat": 40.7128
                }
            ]
        }
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_returns_200(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_weather_forecast5days = AsyncMock(return_value=[])

        response = await async_client.get(
            "/api/data/forecast5/", params=BASE_PARAMS, headers=auth_headers
        )
        assert response.status_code == 200
        openweathermap_srv.get_weather_forecast5days.assert_called_once_with(
            BASE_PARAMS["lat"], BASE_PARAMS["lon"]
        )

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_weather_forecast5days = AsyncMock(
            side_effect=Exception("service error")
        )

        response = await async_client.get(
            "/api/data/forecast5/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.get(
            "/api/data/forecast5/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_returns_200(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_weather_forecast5days_ld = AsyncMock(
            return_value={"@context": {}}
        )

        response = await async_client.get(
            "/api/linkeddata/forecast5/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_weather_forecast5days_ld = AsyncMock(
            side_effect=Exception("service error")
        )

        response = await async_client.get(
            "/api/linkeddata/forecast5/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.get(
            "/api/linkeddata/forecast5/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_weather_returns_200(
        self, async_client, openweathermap_srv, auth_headers, mock_weather_data_out
    ):
        openweathermap_srv.get_weather = AsyncMock(return_value=mock_weather_data_out)

        response = await async_client.get(
            "/api/data/weather/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_get_weather_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_weather = AsyncMock(
            side_effect=Exception("service error")
        )

        response = await async_client.get(
            "/api/data/weather/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_weather_returns_403_without_auth(self, async_client):
        response = await async_client.get(
            "/api/data/weather/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_thi_returns_200(
        self, async_client, openweathermap_srv, auth_headers, mock_thi_data_out
    ):
        openweathermap_srv.get_thi = AsyncMock(return_value=mock_thi_data_out)

        response = await async_client.get(
            "/api/data/thi/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_get_thi_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_thi = AsyncMock(
            side_effect=Exception("service error")
        )

        response = await async_client.get(
            "/api/data/thi/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_thi_returns_403_without_auth(self, async_client):
        response = await async_client.get(
            "/api/data/thi/", params=BASE_PARAMS
        )

        assert response.status_code == 403


    @pytest.mark.anyio
    async def test_get_thi_ld_returns_200(
        self, async_client, openweathermap_srv, auth_headers, mock_jsonld_response
    ):
        # ocsm=True path — returns jsonld
        openweathermap_srv.get_thi = AsyncMock(return_value=mock_jsonld_response)

        response = await async_client.get(
            "/api/linkeddata/thi/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200
        # Verify ocsm=True was passed through
        openweathermap_srv.get_thi.assert_called_once_with(
            BASE_PARAMS["lat"], BASE_PARAMS["lon"], ocsm=True
        )

    @pytest.mark.anyio
    async def test_get_thi_ld_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_thi = AsyncMock(
            side_effect=Exception("service error")
        )

        response = await async_client.get(
            "/api/linkeddata/thi/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_thi_ld_returns_403_without_auth(self, async_client):
        response = await async_client.get(
            "/api/linkeddata/thi/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_all_uavs_returns_200(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_flight_forecast_for_all_uavs = AsyncMock(
            return_value=[]
        )

        response = await async_client.get(
            "/api/data/flight-forecast5/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_all_uavs_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):


        openweathermap_srv.get_flight_forecast_for_all_uavs = AsyncMock(
            side_effect=HTTPException(status_code=500, detail="service error")
        )

        response = await async_client.get(
            "/api/data/flight-forecast5/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_all_uavs_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.get(
            "/api/data/flight-forecast5/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_uav_returns_200(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_flight_forecast_for_uav = AsyncMock(return_value=[])

        response = await async_client.get(
            "/api/data/flight-forecast5/DJI/",
            params=BASE_PARAMS,
            headers=auth_headers,
        )

        assert response.status_code == 200
        openweathermap_srv.get_flight_forecast_for_uav.assert_called_once_with(
            BASE_PARAMS["lat"], BASE_PARAMS["lon"], "DJI"
        )

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_uav_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_flight_forecast_for_uav = AsyncMock(
            side_effect=HTTPException(status_code=500, detail="service error")
        )

        response = await async_client.get(
            "/api/data/flight-forecast5/DJI/",
            params=BASE_PARAMS,
            headers=auth_headers,
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_flight_forecast_for_uav_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.get(
            "/api/data/flight-forecast5/DJI/", params=BASE_PARAMS
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_spray_forecast_returns_200(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_spray_forecast = AsyncMock(return_value=[])

        response = await async_client.get(
            "/api/data/spray-forecast/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_get_spray_forecast_returns_500_on_error(
        self, async_client, openweathermap_srv, auth_headers
    ):
        openweathermap_srv.get_spray_forecast = AsyncMock(
            side_effect=HTTPException(status_code=500, detail="service error")
        )

        response = await async_client.get(
            "/api/data/spray-forecast/", params=BASE_PARAMS, headers=auth_headers
        )

        assert response.status_code == 500

    @pytest.mark.anyio
    async def test_get_spray_forecast_returns_403_without_auth(self, async_client):
        response = await async_client.get(
            "/api/data/spray-forecast/", params=BASE_PARAMS
        )

        assert response.status_code == 403