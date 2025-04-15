from uuid import UUID
from pydantic import BaseModel

from src.schemas.point import GeoJSONOut


class WeatherDataOut(BaseModel):
    id: UUID
    spatial_entity: GeoJSONOut
    data: dict


class THIDataOut(BaseModel):
    id: UUID
    spatial_entity: GeoJSONOut
    thi: float
