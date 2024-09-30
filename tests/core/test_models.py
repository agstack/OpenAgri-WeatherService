import pytest

from tests.fixtures import *
from pydantic import ValidationError

from src.models.point import Point
from src.models.prediction import Prediction
from src.models.weather_data import WeatherData

class TestModels:

    @pytest.mark.anyio
    async def test_point_model_valid(self, app):
        valid_point = {
            "title": "Point title",
            "type": "field",
            "location": {
                "type": "Point",
                "coordinates": [55.43989, 43.121]
            }
        }
        point = Point(**valid_point)
        assert point.title == "Point title"
        assert point.location.type == "Point"

    @pytest.mark.anyio
    async def test_point_model_invalid_point_type(self, app):
        invalid_point = {
            "title": "Point title",
            "type": "lala",
            "location": {
                "type": "Point",
                "coordinates": [55.43989, 43.121]
            }
        }
        with pytest.raises(ValidationError):
            Point(**invalid_point)

    @pytest.mark.anyio
    async def test_prediction_model_valid(self, app):
        valid_prediction = {
                "value": 32.3,
                "timestamp": "2024-06-21T15:00:00.000Z",
                "source": "openweathermaps",
                "data_type": "weather",
                "measurement_type": "ambient_temperature",
                "spatial_entity": {
                    "id": "bad6cd67-638f-42d8-82b8-d4d191174dd6",
                    "type": "POI",
                    "location": {
                        "type": "Point",
                        "coordinates": [ 39.1436, 26.40518]
                    },
                },
            }
        prediction = Prediction(**valid_prediction)
        assert prediction.spatial_entity.location.type == "Point"
        assert hasattr(prediction, 'created_at')
        assert prediction.value == 32.3

    @pytest.mark.anyio
    async def test_weatherdata_model_valid(self, app):
        valid_weeatherdata = {
                "spatial_entity": {
                    "id": "0b1b7964-8f89-465c-a8b2-3d50a53459e0",
                    "type": "POI",
                    "location": {
                        "type": "Point",
                        "coordinates": [ 39.1436, 26.40518]
                    },
                },
                "data": {}
            }
        weatherdata = WeatherData(**valid_weeatherdata)
        assert weatherdata.spatial_entity.location.coordinates == [39.1436, 26.40518]
        assert weatherdata.spatial_entity.location.type == "Point"
        assert isinstance(weatherdata.data, dict)

    @pytest.mark.anyio
    async def test_weatherdata_model_not_valid_point_type(self, app):
        valid_weeatherdata = {
                "spatial_entity": {
                    "id": "0b1b7964-8f89-465c-a8b2-3d50a53459e0",
                    "type": "routa",
                    "location": {
                        "type": "Point",
                        "coordinates": [ 39.1436, 26.40518]
                    },
                },
                "data": {}
            }
        with pytest.raises(ValidationError):
            WeatherData(**valid_weeatherdata)

