from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.external_services import openweathermap
from src.models.prediction import Prediction
from src.models.point import Point


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
    
    @pytest.mark.anyio
    async def test_get_thi_ocm_set_to_false_saves_and_returns_weather_data(
        self,
        openweathermap_srv,
    ):
        mock_weather_data = MagicMock()
        openweathermap_srv.save_weather_data_thi = AsyncMock(return_value=mock_weather_data)

        result = await openweathermap_srv.get_thi(40.7128, -74.0060, ocsm=False)

        openweathermap_srv.save_weather_data_thi.assert_called_once_with(40.7128, -74.0060)
        assert result == mock_weather_data
    
    @pytest.mark.anyio
    async def test_get_thi_ocm_set_to_true_saves_and_returns_weather_data_jsonld(
        self,
        openweathermap_srv,
    ):
        mock_weather_data = MagicMock()
        openweathermap_srv.save_weather_data_thi = AsyncMock(return_value=mock_weather_data)
        mock = MagicMock(return_value={"@context": {}})
        openweathermap.InteroperabilitySchema.weather_data_to_jsonld = mock
        result = await openweathermap_srv.get_thi(40.7128, -74.0060, ocsm=True)

        openweathermap.InteroperabilitySchema.weather_data_to_jsonld.assert_called_once_with(mock_weather_data)
        assert result == {"@context": {}}

    

