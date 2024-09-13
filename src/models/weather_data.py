from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field

from src.models.point import Point


class WeatherData(Document):
    id: UUID = Field(default_factory=uuid4)
    spatial_entity: Point
    data: dict
    created_at: datetime = Field(default_factory=datetime.now) # type: ignore

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": "bad6cd67-638f-42d8-82b8-d4d191174dd6",
                "spatial_entity": {
                    "id": "0b1b7964-8f89-465c-a8b2-3d50a53459e0",
                    "type": "Point",
                    "location": [39.14367, 45.3123]
                },
                "data": {}
            }
        }

    class Settings:
        name = "weather_data"