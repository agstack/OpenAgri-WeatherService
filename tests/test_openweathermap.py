from fastapi import HTTPException
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime, timedelta
from httpx import HTTPError

from src.external_services import openweathermap
from src.external_services.openweathermap import SourceError
from src.models.prediction import Prediction
from src.models.point import Point
from src.models.weather_data import WeatherData


# Fixtures for tests
@pytest.fixture
async def openweathermap_srv():
    dao_mock = AsyncMock()
    owm_srv = openweathermap.OpenWeatherMap()
    owm_srv.setup_dao(dao_mock)
    yield owm_srv


class TestOpenWeatherMap:
    """Test OpenWeatherMap service with mocked external APIs"""
    # Test when cached predictions are older than 3 hours (Should Fail)
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_old_predictions(self, openweathermap_srv):
        old_prediction = Prediction(
            value=42,
            measurement_type="type",
            timestamp=datetime.now(),
            created_at=datetime.now() - timedelta(hours=3, minutes=1),  # Just over 3 hours
            data_type='weather',
            source='openweathermaps',
            spatial_entity=Point(type="station")
        )
        new_prediction = Prediction(
            value=42,
            measurement_type="type",
            timestamp=datetime.now(),
            data_type='weather',
            source='openweathermaps',
            spatial_entity=Point(type="station")
        )

        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        openweathermap_srv.dao.find_or_create_point.return_value = Point(type="station")

        mock_get = AsyncMock(return_value={})
        openweathermap.utils.http_get = mock_get

        mock_parseForecast5dayResponse = AsyncMock(return_value=[new_prediction])
        openweathermap_srv.parseForecast5dayResponse = mock_parseForecast5dayResponse

        lat, lon = (42.424242, 24.242424)
        result = await openweathermap_srv.get_weather_forecast5days(lat, lon)

        assert isinstance(result, list)
        assert len(result) == 1  # No predictions should be returned since it's too old


    # Test if the service raises a SourceError when the HTTP request fails.
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_http_get_throws_error(
        self, openweathermap_srv
    ):
        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        openweathermap_srv.dao.find_or_create_point.return_value = Point(type="station")

        error = HTTPError("Http error")
        error.request = type("Request", (object,), dict({"url": "http://test.url"}))
        mock_get = AsyncMock(side_effect=error)
        openweathermap.utils.http_get = mock_get

        lat, lon = (42.424242, 24.242424)
        with pytest.raises(SourceError):
            await openweathermap_srv.get_weather_forecast5days(lat, lon)

    # Test if a generic exception during response parsing is caught.
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_cathes_generic_exception(
        self, openweathermap_srv
    ):
        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        openweathermap_srv.dao.find_or_create_point.return_value = Point(type="station")

        mock = AsyncMock(side_effect=Exception)
        openweathermap_srv.parseForecast5dayResponse = mock

        lat, lon = (42.424242, 24.242424)
        with pytest.raises(Exception):
            await openweathermap_srv.get_weather_forecast5days(lat, lon)

    # Test the service’s LD (Linked Data) response.
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld(self, openweathermap_srv):
        prediction = Prediction(
            value=42,
            measurement_type="type",
            timestamp=datetime.now(),
            data_type="weather",
            source="openweathermaps",
            spatial_entity=Point(type="station"),
        )
        openweathermap_srv.dao.find_predictions_for_point.return_value = [prediction]
        openweathermap_srv.dao.find_point.return_value = Point(type="station")

        mock = MagicMock(
            return_value={
                "@context": {},
            }
        )
        openweathermap.InteroperabilitySchema.predictions_to_jsonld = mock

        lat, lon = (42.424242, 24.242424)

        result = await openweathermap_srv.get_weather_forecast5days_ld(lat, lon)
        assert isinstance(result, dict)
        assert "@context" in result

    # Test exception handling for get_weather_forecast5days_ld.
    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_catches_exception(
        self, openweathermap_srv
    ):
        openweathermap_srv.dao.find_predictions_for_point.side_effect = Exception

        lat, lon = (42.424242, 24.242424)
        with pytest.raises(Exception):
            await openweathermap_srv.get_weather_forecast5days_ld(lat, lon)