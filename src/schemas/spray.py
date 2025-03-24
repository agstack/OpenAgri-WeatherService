from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel

from src.models.point import GeoJSONTypeEnum
from src.models.spray import SprayStatus


class LocationResponse(BaseModel):
    type: GeoJSONTypeEnum
    coordinates: List

class SprayForecastResponse(BaseModel):
    timestamp: datetime
    spray_conditions: SprayStatus
    weather_source: str
    location: LocationResponse
    detailed_status: Dict[str, str]
