from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.external_services import openweathermap
from src.models.point import Point
from src.models.prediction import Prediction


class TestOpenWeatherMap:
    """Focused tests for OpenWeatherMap unique behaviors (LD output, parse errors)."""

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_catches_generic_exception(
        self, openweathermap_srv
    ):
        openweathermap_srv.dao.find_predictions_for_point.return_value = []
        openweathermap_srv.dao.find_or_create_point.return_value = Point(type="station")

        openweathermap_srv.parseForecast5dayResponse = AsyncMock(side_effect=Exception)

        lat, lon = (42.424242, 24.242424)
        with pytest.raises(Exception):
            await openweathermap_srv.get_weather_forecast5days(lat, lon)

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

        mock = MagicMock(return_value={"@context": {}})
        openweathermap.InteroperabilitySchema.predictions_to_jsonld = mock

        lat, lon = (42.424242, 24.242424)
        result = await openweathermap_srv.get_weather_forecast5days_ld(lat, lon)
        assert isinstance(result, dict)
        assert "@context" in result

    @pytest.mark.anyio
    async def test_get_weather_forecast5days_ld_catches_exception(
        self, openweathermap_srv
    ):
        openweathermap_srv.dao.find_predictions_for_point.side_effect = Exception

        lat, lon = (42.424242, 24.242424)
        with pytest.raises(Exception):
            await openweathermap_srv.get_weather_forecast5days_ld(lat, lon)
