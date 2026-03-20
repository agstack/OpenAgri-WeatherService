import pytest
from datetime import date, datetime
from unittest.mock import AsyncMock, patch


BASE_QUERY = {
    "lat": 40.7128,
    "lon": -74.0060,
    "start": "2024-01-01",
    "end": "2024-01-02",
    "variables": ["temperature_2m"],
    "radius_km": 10.0
}

class TestHistoryRoutes:
    """
    Tests for /api/v1/history/ routes.

    Both routes use MongoDB $near geospatial queries which mongomock does not
    support! We test the cache miss path only  `find_one` is patched to return
    None, triggering the Open-Meteo fallback. The cache hit path (reading from
    DB) requires a real MongoDB instance and is intentionally skipped.
    """

    @pytest.fixture
    def mock_hourly_observation(self):
        """Single hourly observation — reusable unit of hourly data."""
        return {
            "timestamp": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
            "values": {
                "temperature_2m": 25.5,
                "humidity_2m": 60.0,
                "wind_speed_2m": 5.2
            }
        }

    @pytest.fixture
    def mock_daily_observation(self):
        """Single daily observation — reusable unit of daily data."""
        return {
            "date": date(2024, 1, 1).isoformat(),
            "values": {
                "temperature_2m_max": 28.0,
                "temperature_2m_min": 15.0,
                "humidity_2m_max": 70.0
            }
        }

    @pytest.fixture
    def mock_hourly_response(self, mock_hourly_observation):
        return {
            "location": {"lat": 40.7128, "lon": -74.0060},
            "data": [mock_hourly_observation],
            "source": "openmeteo"
        }


    @pytest.fixture
    def mock_daily_response(self, mock_daily_observation):
        """
        Shaped like DailyResponse.
        Same principle as mock_hourly_response.
        """
        return {
            "location": {"lat": 40.7128, "lon": -74.0060},
            "data": [mock_daily_observation],
            "source": "openmeteo"
        }

    @pytest.mark.anyio
    async def test_get_hourly_history_cache_miss_fetches_from_openmeteo(
        self, async_client, auth_headers, mock_hourly_response
    ):
        mock_provider = AsyncMock()
        mock_provider.get_hourly_history.return_value = \
            mock_hourly_response["data"]

        with patch(
            "src.api.api_v1.endpoints.history.HourlyHistory.find_one",
            new_callable=AsyncMock,
            return_value=None  # cache miss
        ), patch(
            "src.api.api_v1.endpoints.history.WeatherClientFactory.get_provider",
            return_value=mock_provider
        ):
            response = await async_client.post(
                "/api/v1/history/hourly/",
                json=BASE_QUERY,
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "openmeteo"
        assert data["location"] == {"lat": BASE_QUERY["lat"], "lon": BASE_QUERY["lon"]}
        mock_provider.get_hourly_history.assert_called_once_with(
            BASE_QUERY["lat"],
            BASE_QUERY["lon"],
            date.fromisoformat(BASE_QUERY["start"]),
            date.fromisoformat(BASE_QUERY["end"]),
            BASE_QUERY["variables"],
        )

    @pytest.mark.anyio
    async def test_get_hourly_history_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.post(
            "/api/v1/history/hourly/", json=BASE_QUERY
        )
        assert response.status_code == 403

    @pytest.mark.skip(
        reason="Cache hit path uses $near geospatial query via find_one and "
               "find_many — not supported by mongomock. Would require a real MongoDB."
    )
    async def test_get_hourly_history_cache_hit_returns_db_data(self):
        pass

    @pytest.mark.anyio
    async def test_get_daily_history_cache_miss_fetches_from_openmeteo(
        self, async_client, auth_headers, mock_daily_response
    ):
        mock_provider = AsyncMock()
        mock_provider.get_daily_history.return_value = \
            mock_daily_response["data"]

        with patch(
            "src.api.api_v1.endpoints.history.DailyHistory.find_one",
            new_callable=AsyncMock,
            return_value=None  # cache miss
        ), patch(
            "src.api.api_v1.endpoints.history.WeatherClientFactory.get_provider",
            return_value=mock_provider
        ):
            response = await async_client.post(
                "/api/v1/history/daily/",
                json=BASE_QUERY,
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "openmeteo"
        assert data["location"] == {"lat": BASE_QUERY["lat"], "lon": BASE_QUERY["lon"]}
        mock_provider.get_daily_history.assert_called_once_with(
            BASE_QUERY["lat"],
            BASE_QUERY["lon"],
            date.fromisoformat(BASE_QUERY["start"]),
            date.fromisoformat(BASE_QUERY["end"]),
            BASE_QUERY["variables"],
        )

    @pytest.mark.anyio
    async def test_get_daily_history_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.post(
            "/api/v1/history/daily/", json=BASE_QUERY
        )
        assert response.status_code == 403

    @pytest.mark.skip(
        reason="Cache hit path uses $near geospatial query via find_one and "
               "find_many — not supported by mongomock. Would require a real MongoDB."
    )
    async def test_get_daily_history_cache_hit_returns_db_data(self):
        pass