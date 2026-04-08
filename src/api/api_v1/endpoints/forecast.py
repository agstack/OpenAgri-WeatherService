"""
Hourly forecast endpoints.

Returns all 24 hours of the current day (past and future) plus the
following days, one record per hour.  No past-hour filtering is applied
so callers always receive a complete day timeline.

Endpoints
---------
GET /api/v1/forecast/hourly/
    Plain JSON – hourly weather data for ``days`` days (default 5).

GET /api/v1/forecast/hourly/spray/
    Hourly spray-condition assessment derived from the same hourly
    forecast, evaluated for every single hour (not tri-hourly).
"""

import logging
from typing import Dict, List

from fastapi import APIRouter, Query, HTTPException

from src.external_services.openmeteo import WeatherClientFactory
from src.schemas.point import GeoJSONOut
from src.schemas.history_data import DailyResponse, HourlyObservationOut, HourlyResponse
from src.schemas.spray import SprayForecastResponse
from src.models.spray import SprayStatus
from src import utils

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# Hourly weather forecast
# ---------------------------------------------------------------------------

@router.get(
    "/hourly/",
    response_model=HourlyResponse,
    summary="Hourly weather data – today (full day) + next days",
)
async def get_hourly_forecast(
    lat: float = Query(..., description="Latitude", example=38.25),
    lon: float = Query(..., description="Longitude", example=21.74),
    days: int = Query(
        5, ge=1, le=16,
        description="Number of days (including today)",
    ),
):
    """
    Returns **hourly** weather data from 00:00 of today through 23:00
    of the last forecast day.

    Unlike the legacy ``/api/data/forecast5/`` endpoint:

    * Resolution is **1 hour** (not 3 hours).
    * **All hours of today** are included – both past and future –
      so the caller always receives a complete timeline for the
      current day.
    * Data comes from the Open-Meteo Forecast API (no API key required).
    """
    client = WeatherClientFactory.get_provider()
    try:
        results = await client.get_hourly_forecast(lat, lon, days=days)
    except Exception as e:
        logger.error(f"Error fetching hourly forecast from Open-Meteo: {e}")
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve hourly forecast from Open-Meteo",
        ) from e

    return HourlyResponse(
        location={"lat": lat, "lon": lon},
        data=results,
        source="open-meteo",
    )


# ---------------------------------------------------------------------------
# Hourly spray-condition forecast
# ---------------------------------------------------------------------------

@router.get(
    "/hourly/spray/",
    response_model=List[SprayForecastResponse],
    summary="Hourly spray-condition forecast – today (full day) + next days",
)
async def get_hourly_spray_forecast(
    lat: float = Query(..., description="Latitude", example=38.25),
    lon: float = Query(..., description="Longitude", example=21.74),
    days: int = Query(
        5, ge=1, le=16,
        description="Number of days (including today)",
    ),
):
    """
    Evaluates **hourly** spray conditions from 00:00 of today through 23:00
    of the last forecast day.

    Each hour is individually assessed for temperature, wind, humidity,
    precipitation and delta-T to produce an ``optimal``, ``marginal``,
    or ``unsuitable`` rating.

    All hours of the current day (past and future) are included so the
    caller always gets a complete day timeline.
    """
    client = WeatherClientFactory.get_provider()
    try:
        hourly_data = await client.get_hourly_forecast(lat, lon, days=days)
    except Exception as e:
        logger.error(f"Error fetching hourly forecast from Open-Meteo: {e}")
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve hourly forecast from Open-Meteo",
        ) from e

    location = GeoJSONOut(**{"type": "Point", "coordinates": [lat, lon]})

    results: List[SprayForecastResponse] = []
    for obs in hourly_data:
        v = obs.values
        temp = v.get("temperature_2m")
        humidity = v.get("relative_humidity_2m")
        wind_ms = v.get("wind_speed_10m")
        precipitation = v.get("precipitation", 0.0) or 0.0

        # Instead of skipping the hour entirely if one variable is missing, we could
        # choose to evaluate spray conditions with the available data and mark the missing
        # variables in the detailed status.
        if temp is None or humidity is None or wind_ms is None:
            logger.warning(f"Missing essential weather data for hour {obs.timestamp}: temp={temp}, humidity={humidity}, wind_ms={wind_ms}")
            spray_condition = "unknown"
            status_details = {
                "temperature": temp if temp is not None else "missing",
                "humidity": humidity if humidity is not None else "missing",
                "wind_speed": wind_ms if wind_ms is not None else "missing",
                "precipitation": precipitation,
            }
        else:

            wind_kmh = wind_ms * 3.6  # convert m/s → km/h
            temp_wet_bulb = utils.calculate_wet_bulb(temp, humidity)
            delta_t = temp - temp_wet_bulb

            spray_condition, status_details = utils.evaluate_spray_conditions(
                temp, wind_kmh, precipitation, humidity, delta_t,
            )

        # Convert SprayStatus enum values to strings for the dict
        detailed_status_str: Dict[str, str] = {
            k: v.value if isinstance(v, SprayStatus) else str(v)
            for k, v in status_details.items()
        }

        results.append(
            SprayForecastResponse(
                timestamp=obs.timestamp,
                spray_conditions=spray_condition,
                source="open-meteo",
                location=location,
                detailed_status=detailed_status_str,
            )
        )

    return results


# ---------------------------------------------------------------------------
# Daily irrigation forecast
# ---------------------------------------------------------------------------

@router.get(
    "/daily/irrigation/",
    response_model=DailyResponse,
    summary="Daily weather forecast for smart irrigation (1–16 days)",
)
async def get_daily_irrigation_forecast(
    lat: float = Query(..., description="Latitude", example=38.25),
    lon: float = Query(..., description="Longitude", example=21.74),
    days: int = Query(
        16, ge=1, le=16,
        description="Number of forecast days (including today)",
    ),
):
    """
    Returns **daily** weather data optimized for smart irrigation systems.

    Variables returned per day:
    - **precipitation_sum** – total precipitation (mm)
    - **precipitation_probability_max** – maximum precipitation probability (%)
    - **temperature_2m_min** – minimum temperature (°C)
    - **temperature_2m_max** – maximum temperature (°C)
    - **et0_fao_evapotranspiration** – reference evapotranspiration ET₀ (mm)

    Data comes from the Open-Meteo Forecast API.
    Supports up to 16 days of forecast.
    """
    client = WeatherClientFactory.get_provider()
    try:
        results = await client.get_daily_forecast(lat, lon, days=days)
    except Exception as e:
        logger.error(f"Error fetching daily forecast from Open-Meteo: {e}")
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve daily forecast from Open-Meteo",
        ) from e

    return DailyResponse(
        location={"lat": lat, "lon": lon},
        data=results,
        source="open-meteo",
    )
