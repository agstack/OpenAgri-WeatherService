import logging
from typing import List
from uuid import uuid4

from beanie.odm.operators.find.logical import And

from src.models.point import Point, GeoJSON, PointTypeEnum, GeoJSONTypeEnum
from src.models.prediction import Prediction
from src.models.weather_data import WeatherData


logger = logging.getLogger(__name__)

class Dao():

    def __init__(self, db_client):
        self.db = db_client

    async def add_dummy_point(self) -> Point:
        try:
          geojson_obj = GeoJSON(type=GeoJSONTypeEnum.POINT, coordinates=[15.520541, 8.25478])
          logger.debug(geojson_obj)
          __point = Point(id=str(uuid4()), type=PointTypeEnum.POI, location=geojson_obj)
          new_point = await __point.create()
          return new_point
        except Exception as e:
            logger.error("Somenthing happened. Point not added!")
            logger.exception(e)
            raise e

    async def find_point(self, lat: float, lon: float) -> Point:
        return await Point.find_one(And(Point.location.coordinates == [lat, lon], Point.location.type == GeoJSONTypeEnum.POINT))

    async def create_point(self, lat: float, lon: float) -> Point:
        return await Point(**{'type': PointTypeEnum.POI, 'location': GeoJSON(**{'coordinates': [lat, lon], 'type': GeoJSONTypeEnum.POINT})}).create()

    async def find_predictions_for_point(self, lat, lon) -> List[Prediction]:
        point = await Point.find_one(And(Point.location.coordinates == [lat, lon], Point.location.type == GeoJSONTypeEnum.POINT))
        if not point:
            return []

        logger.debug("Location was cached")
        return await Prediction.find(Prediction.spatial_entity == point).to_list()

    async def find_prediction_for_radius(self, lat: float, lon: float) -> List[Prediction]:
        ...

    async def find_weather_data_for_point(self, lat, lon) -> WeatherData:
        point = await Point.find_one(And(Point.location.coordinates == [lat, lon], Point.location.type == GeoJSONTypeEnum.POINT))
        if not point:
            return None

        logger.debug("Location was cached")
        return await WeatherData.find_one(WeatherData.spatial_entity == point)
    
    async def save_weather_data_for_point(self, data: dict, point: Point) -> WeatherData:
        return await WeatherData(data=data, spatial_entity=point).create()
