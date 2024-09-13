import logging

import httpx

from src.core import config
from src import utils
from src.core.dao import Dao
from src.models.point import Point, GeoJSON, GeoJSONTypeEnum
from src.models.prediction import Prediction
from src.interoperability import InteroperabilitySchema


logger = logging.getLogger(__name__)

class SourceError(Exception):
   ...

class OpenWeatherMap():

    properties = {
        'service': 'openWeatherMaps',
        'operation': 'weatherForecast',
        'dataClassification': 'prediction',
        'dataType': 'weather',
        'endpointURI': 'http://api.openweathermap.org/data/2.5',
        'documentationURI': 'https://openweathermap.org/forecast5',
        'dataExpiration': 3000,
        'dataProximityRadius': 100,
        'extracted_schema': {
            'period': {
                'timestamp': ['dt'],
                # 'datetime': ['dt_txt'],
            },
            'measurements': {
                'ambient_temperature': ['main', 'temp'],
                'ambient_humidity': ['main', 'humidity'],
                'wind_speed': ['wind', 'speed'],
                'wind_direction': ['wind', 'deg'],
                'precipitation': ['rain', '3h'],
            }
        },
    }

    def __init__(self):
       self.dao = None

    def setup_dao(self, dao: Dao):
       self.dao = dao

    async def get_weather_forecast5days(self, lat: float, lon: float) -> dict:
        try:
            predictions = await self.dao.find_predictions_for_point(lat, lon)
            if predictions:
                return predictions

            point = await self.dao.create_point(lat, lon)
            url = f'{self.properties["endpointURI"]}/forecast?units=metric&lat={lat}&lon={lon}&appid={config.OPENWEATHERMAP_API_KEY}'
            openweathermap_json = await utils.http_get(url)
            predictions = await self.parseForecast5dayResponse(point, openweathermap_json)
        except httpx.HTTPError as httpe:
           logger.exception(httpe)
           raise SourceError(f"Request to {httpe.request.url} was not succesful")
        except Exception as e:
           logger.exception(e)
           raise e
        else:
            return predictions

    async def get_weather_forecast5days_ld(self, lat: float, lon: float) -> dict:
        try:
            predictions = await self.get_weather_forecast5days(lat, lon)
            point = await self.dao.find_point(lat, lon)
            jsonld_data = InteroperabilitySchema.serialize(predictions, point)
        except Exception as e:
           logger.exception(e)
           raise e

        return jsonld_data

    async def get_thi(self, lat: float, lon: float) -> dict:
        try:
            weather_data = await self.dao.find_weather_data_for_point(lat, lon)
            if not weather_data:
                point = await self.dao.create_point(lat, lon)
                url = f'{self.properties["endpointURI"]}/weather?units=metric&lat={lat}&lon={lon}&appid={config.OPENWEATHERMAP_API_KEY}'
                openweathermap_json = await utils.http_get(url)
                weather_data = await self.dao.save_weather_data_for_point(openweathermap_json, point)
        except httpx.HTTPError as httpe:
           logger.exception(httpe)
           raise SourceError(f"Request to {httpe.request.url} was not succesful")
        except Exception as e:
           logger.exception(e)
           raise e

        temp = weather_data.data["main"]["temp"]
        rh = weather_data.data["main"]["humidity"]
        thi = utils.calculate_thi(temp, rh)
        return {"thi": thi}

    async def get_weather(self, lat: float, lon: float) -> dict:
        try:
            weather_data = await self.dao.find_weather_data_for_point(lat, lon)
            if not weather_data:
                point = await self.dao.create_point(lat, lon)
                url = f'{self.properties["endpointURI"]}/weather?units=metric&lat={lat}&lon={lon}&appid={config.OPENWEATHERMAP_API_KEY}'
                openweathermap_json = await utils.http_get(url)
                weather_data = await self.dao.save_weather_data_for_point(openweathermap_json, point)
        except httpx.HTTPError as httpe:
           logger.exception(httpe)
           raise SourceError(f"Request to {httpe.request.url} was not succesful")
        except Exception as e:
           logger.exception(e)
           raise e

        return weather_data.data

    async def parseForecast5dayResponse(self, point: Point, data: dict) -> dict:

        # Extract data to a list of Predictions
        extracted_data = []
        predictions = []
        try:
          for e in data['list']:
              extracted_element = utils.deepcopy_dict(self.properties['extracted_schema'])
              for key, path in self.properties['extracted_schema']['period'].items():
                extracted_element['period'][key] = utils.extract_value_from_dict_path(e, path)
              for key, path in self.properties['extracted_schema']['measurements'].items():
                extracted_element['measurements'][key] = utils.extract_value_from_dict_path(e, path)
                if not extracted_element['measurements'][key]:
                   continue
                prediction = await Prediction(
                      value=extracted_element['measurements'][key],
                      measurement_type=key,
                      timestamp=extracted_element['period']['timestamp'],
                      data_type='weather',
                      source='openweathermaps',
                      spatial_entity=point
                      ).create()
                predictions.append(prediction)
                extracted_data.append(extracted_element)

        except Exception as e:
            logger.debug("Cannot transform to Linked Data")
            logger.error(e)
        else:
           return predictions

