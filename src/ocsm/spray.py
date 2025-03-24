from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.spray import SprayStatus
from src.ocsm.base import Observation, Result


class SprayForecastResult(Result):
    spray_conditions: str
    temperature: Optional[float] = None
    precipitation: Optional[float] = None
    windSpeed: Optional[float] = None
    atmosphericPressure: Optional[float] = None
    relativeHumidity: Optional[float] = None
    gustSpeed: Optional[float] = None
    deltaT: Optional[float] = None


class SprayForecastDetailedStatus(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(["sprayForecastDetailedStatus"], alias="@type")
    temperatureStatus: SprayStatus
    windStatus: SprayStatus
    precipitationStatus: SprayStatus
    humidityStatus: SprayStatus
    deltaTStatus: SprayStatus


class SprayForecastObservation(Observation):
    type: List[str] = Field(["Observation", "SprayForecast"], alias="@type")
    hasResult: SprayForecastResult
    sprayForecastDetailedStatus: Optional[SprayForecastDetailedStatus] = None
