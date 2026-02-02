import logging
from fastapi import HTTPException
import httpx
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Protocol, Union
import os

from src.core import config
from src.schemas.history_data import DailyObservationOut, HourlyObservationOut


logger = logging.getLogger(__name__)

class WeatherProvider(Protocol):
    async def get_hourly_history(
            self, lat: float, lon: float, start: date, end: date, variables: List[str]
    ) -> List[HourlyObservationOut]:
        ...

    async def get_daily_history(
            self, lat: float, lon: float, start: date, end: date, variables: List[str]
    ) -> List[DailyObservationOut]:
        ...

    async def get_hourly_forecast(
            self, lat: float, lon: float, days: int = 5
    ) -> List[HourlyObservationOut]:
        ...


class OpenMeteoClient:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    async def _fetch_data(self, params: dict, url: Optional[str] = None) -> dict:
        """Fetch data from Open-Meteo API with error handling."""
        target_url = url or self.BASE_URL
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(target_url, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except (httpx.NetworkError, httpx.ConnectError, httpx.TimeoutException) as e:
            logger.error(f"Internet connection is not available: {e}")
            raise HTTPException(
                status_code=503,
                detail="Internet connection is not available. Please cache data for the specified location"
            ) from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise e

    async def _fetch_data(self, params: dict) -> dict:
        """Fetch data from Open-Meteo API with error handling."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except (httpx.NetworkError, httpx.ConnectError, httpx.TimeoutException) as e:
            logger.error(f"Internet connection is not available: {e}")
            raise HTTPException(
                status_code=503,
                detail="Internet connection is not available. Please cache data for the specified location"
            ) from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise e

    async def get_hourly_history(self, lat: float, lon: float, start: date, end: date, variables: List[str]) -> List[HourlyObservationOut]:
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(variables),
            "timezone": "auto",
            "start_date": start.isoformat(),
            "end_date": end.isoformat()
        }

        data = await self._fetch_data(params)
        timestamps = data["hourly"]["time"]
        results = []

        for i, t in enumerate(timestamps):
            values = {v: data["hourly"][v][i] for v in variables if v in data["hourly"]}
            results.append(HourlyObservationOut(timestamp=datetime.fromisoformat(t), values=values))

        return results

    async def get_daily_history(self, lat: float, lon: float, start: date, end: date, variables: List[str]) -> List[DailyObservationOut]:
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ",".join(variables),
            "timezone": "auto",
            "start_date": start.isoformat(),
            "end_date": end.isoformat()
        }

        data = await self._fetch_data(params)
        timestamps = data["daily"]["time"]
        results = []

        for i, t in enumerate(timestamps):
            values = {v: data["daily"][v][i] for v in variables if v in data["daily"]}
            results.append(DailyObservationOut(date=date.fromisoformat(t), values=values))

        return results

    async def get_single_day_history(self, lat: float, lon: float, day: date, variables: dict[str, List[str]]) -> tuple[List[HourlyObservationOut], List[DailyObservationOut]]:
        hourly = await self.get_hourly_history(lat, lon, day, day, variables.get("hourly", []))
        daily = await self.get_daily_history(lat, lon, day, day, variables.get("daily", []))
        return hourly, daily

    # ---- Hourly forecast (Open-Meteo Forecast API) ----

    # The list of hourly variables requested from the Open-Meteo Forecast API.
    HOURLY_FORECAST_VARIABLES = [
        "temperature_2m",
        "relative_humidity_2m",
        "dew_point_2m",
        "apparent_temperature",
        "precipitation",
        "rain",
        "snowfall",
        "snow_depth",
        "pressure_msl",
        "surface_pressure",
        "cloud_cover",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
        "visibility",
        "uv_index",
    ]

    async def get_hourly_forecast(
        self, lat: float, lon: float, days: int = 5
    ) -> List[HourlyObservationOut]:
        """
        Fetch hourly weather data for today (all 24 h, past + future) plus
        the next ``days−1`` days from the Open-Meteo **Forecast** API.

        Returns one :class:`HourlyObservationOut` per hour (up to ``days * 24``
        entries).  Past hours of the current day are **never** filtered out so
        the caller always gets a complete day timeline.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(self.HOURLY_FORECAST_VARIABLES),
            "timezone": "auto",
            "past_days": 0,
            "forecast_days": days,
        }

        data = await self._fetch_data(params, url=self.FORECAST_URL)

        if "hourly" not in data:
            logger.warning("Open-Meteo returned no hourly forecast data")
            return []

        timestamps = data["hourly"]["time"]
        results: List[HourlyObservationOut] = []

        for i, t in enumerate(timestamps):
            values: Dict[str, Union[float, None]] = {}
            for var in self.HOURLY_FORECAST_VARIABLES:
                if var in data["hourly"]:
                    values[var] = data["hourly"][var][i]
            results.append(
                HourlyObservationOut(
                    timestamp=datetime.fromisoformat(t),
                    values=values,
                )
            )

        logger.info(
            "Open-Meteo hourly forecast: %d hours for (%s, %s), %d days",
            len(results), lat, lon, days,
        )
        return results


# Factory using environment variable
class WeatherClientFactory:
    _provider: Optional[WeatherProvider] = None

    @classmethod
    def get_provider(cls) -> WeatherProvider:
        if cls._provider is None:
            provider_name = config.HISTORY_WEATHER_PROVIDER
            if provider_name == "openmeteo":
                cls._provider = OpenMeteoClient()
            else:
                raise ValueError(f"Unsupported weather provider: {provider_name}")
        return cls._provider