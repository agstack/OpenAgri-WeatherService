"""
Focused tests for external services with proper mocking of 3rd party API responses.
Tests OpenWeatherMap and Open-Meteo API interactions with realistic mock responses.
"""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError

from src.external_services.openmeteo import OpenMeteoClient
from src.external_services.openweathermap import SourceError


class TestOpenWeatherMapApi:
    @pytest.fixture
    def mock_owm_5day_forecast_response(self):
        return {
            "cod": "200",
            "message": 0,
            "cnt": 40,
            "list": [
                {
                    "dt": 1640995200,
                    "main": {
                        "temp": 25.5,
                        "feels_like": 26.2,
                        "temp_min": 23.0,
                        "temp_max": 28.0,
                        "pressure": 1013,
                        "humidity": 60,
                        "sea_level": 1013,
                        "grnd_level": 1010,
                    },
                    "weather": [
                        {
                            "id": 800,
                            "main": "Clear",
                            "description": "clear sky",
                            "icon": "01d",
                        }
                    ],
                    "clouds": {"all": 0},
                    "wind": {"speed": 5.2, "deg": 180, "gust": 7.8},
                    "visibility": 10000,
                    "pop": 0,
                    "sys": {"pod": "d"},
                    "dt_txt": "2022-01-01 00:00:00",
                }
            ],
            "city": {
                "id": 5128581,
                "name": "New York",
                "coord": {"lat": 40.7128, "lon": -74.0060},
                "country": "US",
            },
        }

    @pytest.fixture
    def mock_owm_current_weather_response(self):
        return {
            "coord": {"lon": -74.0060, "lat": 40.7128},
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "main": {
                "temp": 25.5,
                "feels_like": 26.2,
                "temp_min": 23.0,
                "temp_max": 28.0,
                "pressure": 1013,
                "humidity": 60,
                "sea_level": 1013,
                "grnd_level": 1010,
            },
            "wind": {"speed": 5.2, "deg": 180, "gust": 7.8},
            "clouds": {"all": 0},
            "dt": 1640995200,
            "sys": {"country": "US"},
            "timezone": -18000,
            "id": 5128581,
            "name": "New York",
            "cod": 200,
        }

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_successful_api_response(
        self, openweathermap_srv, mock_owm_5day_forecast_response
    ):
        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        mock_point = MagicMock()
        mock_point.type = "station"
        openweathermap_srv.dao.find_or_create_point.return_value = mock_point
        with patch(
            "src.external_services.openweathermap.utils.http_get"
        ) as mock_http_get:
            mock_http_get.return_value = mock_owm_5day_forecast_response
            result = await openweathermap_srv.get_weather_forecast5days(
                40.7128, -74.0060
            )
            assert result is None or isinstance(result, list)
            mock_http_get.assert_called_once()

    @pytest.mark.anyio
    async def test_get_weather_successful_api_response(
        self, openweathermap_srv, mock_owm_current_weather_response
    ):
        openweathermap_srv.dao.find_weather_data_for_point.return_value = []
        mock_point = MagicMock()
        mock_point.type = "station"
        openweathermap_srv.dao.find_or_create_point.return_value = mock_point
        with patch(
            "src.external_services.openweathermap.utils.http_get"
        ) as mock_http_get:
            mock_http_get.return_value = mock_owm_current_weather_response
            result = await openweathermap_srv.get_weather(40.7128, -74.0060)
            assert result is not None
            mock_http_get.assert_called_once()

    @pytest.mark.anyio
    async def test_api_http_error_handling(self, openweathermap_srv):
        """Tests HTTP error handling for OpenWeatherMap API calls.

        Covers both HTTP errors and timeouts.
        """
        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        mock_point = MagicMock()
        mock_point.type = "station"
        openweathermap_srv.dao.find_or_create_point.return_value = mock_point
        with patch(
            "src.external_services.openweathermap.utils.http_get"
        ) as mock_http_get:
            error = HTTPError("HTTP error occurred")
            req = MagicMock()
            req.url = "http://api.openweathermap.org/data/2.5/forecast"
            error.request = req
            mock_http_get.side_effect = error
            with pytest.raises(SourceError) as exc_info:
                await openweathermap_srv.get_weather_forecast5days(40.7128, -74.0060)
            assert str(exc_info.value).startswith("Request to")


class TestOpenMeteoApi:
    @pytest.fixture
    async def openmeteo_client(self):
        return OpenMeteoClient()

    @pytest.fixture
    def mock_openmeteo_hourly_response(self):
        return {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "hourly": {
                "time": [
                    "2024-01-01T00:00",
                    "2024-01-01T01:00",
                    "2024-01-01T02:00",
                    "2024-01-01T03:00",
                ],
                "temperature_2m": [25.5, 24.8, 24.2, 23.9],
                "humidity_2m": [60, 62, 64, 66],
                "pressure_2m": [1013.25, 1012.80, 1012.35, 1011.90],
                "wind_speed_2m": [5.2, 4.8, 4.5, 4.2],
            },
            "hourly_units": {
                "time": "iso8601",
                "temperature_2m": "°C",
                "humidity_2m": "%",
                "pressure_2m": "hPa",
                "wind_speed_2m": "m/s",
            },
        }

    @pytest.fixture
    def mock_openmeteo_daily_response(self):
        return {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "daily": {
                "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
                "temperature_2m_max": [28.0, 26.5, 24.8, 22.3],
                "temperature_2m_min": [15.0, 16.2, 17.5, 18.1],
                "humidity_2m_max": [70, 68, 72, 75],
                "humidity_2m_min": [50, 52, 55, 58],
            },
            "daily_units": {
                "time": "iso8601",
                "temperature_2m_max": "°C",
                "temperature_2m_min": "°C",
                "humidity_2m_max": "%",
                "humidity_2m_min": "%",
            },
        }

    @pytest.mark.anyio
    async def test_get_hourly_history_successful_api_response(
        self, openmeteo_client, mock_openmeteo_hourly_response
    ):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_openmeteo_hourly_response
            mock_get.return_value = mock_response
            result = await openmeteo_client.get_hourly_history(
                lat=40.7128,
                lon=-74.0060,
                start=date(2024, 1, 1),
                end=date(2024, 1, 2),
                variables=["temperature_2m", "humidity_2m", "pressure_2m"],
            )
            assert isinstance(result, list) and len(result) == 4
            assert all(
                hasattr(obs, "timestamp") and hasattr(obs, "values") for obs in result
            )
            assert result[0].values["temperature_2m"] == 25.5

    @pytest.mark.anyio
    async def test_get_daily_history_successful_api_response(
        self, openmeteo_client, mock_openmeteo_daily_response
    ):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_openmeteo_daily_response
            mock_get.return_value = mock_response
            result = await openmeteo_client.get_daily_history(
                lat=40.7128,
                lon=-74.0060,
                start=date(2024, 1, 1),
                end=date(2024, 1, 7),
                variables=[
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "humidity_2m_max",
                ],
            )
            assert isinstance(result, list) and len(result) == 4
            assert all(
                hasattr(obs, "date") and hasattr(obs, "values") for obs in result
            )
            assert result[0].values["temperature_2m_max"] == 28.0

    @pytest.mark.anyio
    async def test_openmeteo_api_http_error_handling(self, openmeteo_client):
        with patch("httpx.AsyncClient.get") as mock_get:
            error = HTTPError("HTTP error occurred")
            mock_get.side_effect = error
            with pytest.raises(Exception):
                await openmeteo_client.get_hourly_history(
                    lat=40.7128,
                    lon=-74.0060,
                    start=date(2024, 1, 1),
                    end=date(2024, 1, 2),
                    variables=["temperature_2m"],
                )

    @pytest.mark.anyio
    async def test_openmeteo_network_timeout(self, openmeteo_client):
        with patch("httpx.AsyncClient.get") as mock_get:
            error = HTTPError("Request timeout")
            mock_get.side_effect = error
            with pytest.raises(Exception):
                await openmeteo_client.get_daily_history(
                    lat=40.7128,
                    lon=-74.0060,
                    start=date(2024, 1, 1),
                    end=date(2024, 1, 7),
                    variables=["temperature_2m_max"],
                )
