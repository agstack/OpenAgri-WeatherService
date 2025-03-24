from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Union, Optional
from datetime import datetime
from uuid import UUID


class JSONLDGraph(BaseModel):
    context: List[Union[str, dict]] = Field(..., alias="@context")
    graph: List[dict] = Field(..., alias="@graph")


class GeoJSON(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]


class FeatureOfInterest(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(["FeatureOfInterest", "Point"], alias="@type")
    lon: float
    lat: float


class Sensor(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(["Sensor"], alias="@type")
    name: str


class Observation(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(..., alias="@type")
    description: str
    hasFeatureOfInterest: str
    madeBySensor: Optional[str] = None
    weatherSource: str
    resultTime: datetime
    phenomenonTime: datetime


class Result(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(..., alias="@type")
