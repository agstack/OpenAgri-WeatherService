from enum import Enum
from uuid import uuid4, UUID
from typing import Optional, List

from beanie import Document
from pydantic import Field


class PointTypeEnum(str, Enum):
    station = 'station'
    crop = 'crop'
    field = 'field'
    collector = 'collector'
    route = 'route'
    resource = 'resource'
    POI = 'POI'


class GeoJSONTypeEnum(str, Enum):
    POINT = 'Point'
    POLYGON = 'POLYGON'


class GeoJSON(Document):
    id: UUID = Field(default_factory=uuid4)
    type: GeoJSONTypeEnum
    coordinates: List

    class Config:
        use_enum_values = True


class Point(Document):
    id: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    type: PointTypeEnum
    location: Optional[GeoJSON] = None

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": "bad6cd67-638f-42d8-82b8-d4d191174dd6",
                "type": "POI",
                "location": {
                    "id": "0b1b7964-8f89-465c-a8b2-3d50a53459e0",
                    "type": "Point",
                    "location": [39.14367, 45.3123]
                },
            }
        }

    class Settings:
        name = "points"