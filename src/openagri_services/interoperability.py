import logging
from typing import Optional, Union
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


# Observation Related
class MadeBySensorSchema(BaseModel):
    name: str

### QuantityValue Schema (Used for Numeric Values)
class QuantityValueSchema(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(default="QuantityValue", alias="@type")
    unit: Optional[str] = None
    hasValue: Optional[str] = None  # For flight forecast, e.g., "OK"

### HasAgriParcel to define relation with parcel
class HasAgriParcel(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(default="Parcel", alias="@type")

class ObservationSchema(BaseModel):
    id: Optional[str] = Field(default=None, alias="@id")
    type: str = Field(default="Observation", alias="@type")
    activityType: Union[str, dict]
    title: str
    details: str
    phenomenonTime: str
    madeBySensor: Optional[MadeBySensorSchema] = Field(default=None)
    hasAgriParcel: Optional[HasAgriParcel] = Field(default=None)
    hasResult: QuantityValueSchema
    observedProperty: str
