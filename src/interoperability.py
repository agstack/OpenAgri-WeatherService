import logging
from typing import List
import uuid

from src import utils
from src.models.point import Point
from src.models.prediction import Prediction
from src.utils import deepcopy_dict


logger = logging.getLogger(__name__)

# TODO: Re-Implement this class using OCSM
class InteroperabilitySchema:

    context_schema = {
          '@context': {
              '@base': 'http://localhost:5000/api/weatherForecast/weatherForecast5_3/',
              'farmtopia': 'http://localhost:5000/demo/farmtopia.rdf#',
              'sosa': 'http://www.w3.org/ns/sosa/',
              'weather': 'https://bimerr.iot.linkeddata.es/def/weather/#',
              'collections': {
                '@id': 'sosa:hasMember',
                '@type': '@id',
                '@container': '@set',
              },
              'items': {
                '@id': 'sosa:hasMember',
                '@type': '@id',
                '@container': '@set',
              },
              'spatialEntity': {
                '@id': 'sosa:hasFeatureOfInterest',
                '@type': '@id',
              },
              'data_specification': {
                '@id': 'sosa:observedProperty',
                '@type': '@id',
              },
              'unit': {
                '@id': 'farmtopia:unitOfMeasure',
                '@type': '@id',
              },
              'property': {
                '@id': 'sosa:observedProperty',
                '@type': '@id',
              },
              'timestamp': 'sosa:phenomenonTime',
              'value': 'sosa:hasSimpleResult',
              'Temperature': 'weather:temp',
              'Celsius': 'unit:DEG_C',
              'RelativeHumidity': 'weather:RelativeHumidity',
              'Percent': 'unit:PERCENT',
              'WindSpeed': 'weather:WindSpeed',
              'MeterPerSecond': 'unit:M-PER-SEC',
              'WindDirection': 'weather:WindDirection',
              'Degree': 'unit:DEG',
              'Precipitation': 'weather:rain',
              'Millimetre': 'unit:MilliM',
              'Pressure': 'weather:AtmospheriStatisonPressure',
              'Hectopascal': 'unit:HectoPA',
              'Radiation': 'weather:DirectNormalRadiation',
              'WattPerMetre2': 'unit:MicroW-PER-M2',
          }
    }

    item_schema = {
        '@id': '', # "prediction/1",
        # "@type": "prediction",
        '@type': 'farmtopia:Prediction',
        'timestamp': '', # "2024-25-01T06:01:00",
        'value': '', # 91.67
    }

    collection_schema = {
        '@id': '', # "_:collection_1",
        # "@type": "predictionCollection",
        '@type': 'farmtopia:PredictionCollection',
        'spatialEntity': '', # "POIorROI_ID",
        'measurement': '', # "Temperature",
        'unit': '', # "Celsius",
        'items': []
    }

    schema = {
        '@context': context_schema,
        '@id': '',
        'collections': []
    }

    property_schema = { # TODO add these to data_specifications objects on defaults.json
        'ambient_temperature': {
          'measurement': 'Temperature',
          'unit': 'Celsius',
        },
        'ambient_humidity': {
          'measurement': 'RelativeHumidity',
          'unit': 'Percent',
        },
        'wind_speed': {
          'measurement': 'WindSpeed',
          'unit': 'MeterPerSecond',
        },
        'wind_direction': {
          'measurement': 'WindDirection',
          'unit': 'Degree',
        },
        'precipitation': {
          'measurement': 'Precipitation',
          'unit': 'Millimetre',
        },
    }

    @classmethod
    def serialize(cls, predictions: List[Prediction], spatial_entity: Point) -> dict:
        collection_schema = cls.collection_schema
        item_schema = cls.item_schema
        property_schema = cls.property_schema

        semantic_data = utils.deepcopy_dict(cls.schema)
        spatial_entity = str(spatial_entity.id)
        collection_idx = 0
        serialized_collections = {}
        try:
            for pred in predictions:
                collection_key = property_schema[pred.measurement_type]['measurement']
                item = deepcopy_dict(item_schema)
                item['@id'] = str(pred.id)
                item['timestamp'] = str(pred.timestamp)
                item['value'] = pred.value
                if collection_key in serialized_collections:
                    serialized_collections[collection_key]['items'].append(item)
                    continue

                collection = utils.deepcopy_dict(collection_schema)
                collection['@id'] = f'_:collection_{collection_idx}'
                collection_idx += 1
                collection['spatialEntity'] = spatial_entity
                collection['measurement'] = collection_key
                collection['unit'] = property_schema[pred.measurement_type]['unit']
                collection['items'].append(item)
                serialized_collections[collection_key] = collection

            semantic_data['@id'] = str(uuid.uuid4())
            semantic_data['collections'].extend(list(serialized_collections.values()))

            return semantic_data
        except Exception as e:
            logger.exception(e)