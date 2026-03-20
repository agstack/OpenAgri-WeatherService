import pytest
from unittest.mock import AsyncMock, patch
from src.models.history_data import CachedLocation

MOCK_LAT = 40.7128
MOCK_LON = -74.0060

class TestLocationRoutes:
    """
    Integration tests for /api/v1/locations/ routes.
    Uses the in-memory MongoDB (AsyncMongoMockClient) via the app fixture.
    Data is inserted directly into the mock DB before each test that needs it.

    NOTE: exists-in-radius is skipped — it relies on MongoDB $near geospatial
    queries which are not supported by mongomock.
    """

    # Runs after every test to keep the DB clean.
    @pytest.fixture(autouse=True)
    async def clean_db(self):
        yield
        await CachedLocation.find_all().delete()

    # Inserts a real CachedLocation document into the mock DB.
    # Returns the inserted document so tests can reference its id.
    async def _insert_location(self, name="Test Location", location=dict):
        doc = CachedLocation(name=name, location=location)
        await doc.insert()
        return doc

    @pytest.mark.anyio
    async def test_list_locations_returns_200_with_empty_db(
        self, async_client, auth_headers
    ):
        response = await async_client.get(
            "/api/v1/locations/locations/", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.anyio
    async def test_list_locations_returns_inserted_documents(
        self, async_client, auth_headers, mock_location
    ):
        await self._insert_location("Location A", location=mock_location)
        await self._insert_location("Location B", location=mock_location)

        response = await async_client.get(
            "/api/v1/locations/locations/", headers=auth_headers
        )

        assert response.status_code == 200
        assert len(response.json()) == 2
        names = [loc["name"] for loc in response.json()]
        assert "Location A" in names
        assert "Location B" in names

    @pytest.mark.anyio
    async def test_list_locations_returns_403_without_auth(self, async_client):
        response = await async_client.get("/api/v1/locations/locations/")
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_location_by_coordinates_returns_200(
        self, async_client, auth_headers, mock_location
    ):
        await self._insert_location(location=mock_location)

        response = await async_client.get(
            "/api/v1/locations/locations/by-coordinates/",
            params={"lat": MOCK_LAT, "lon": MOCK_LON},
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json()["lat"] == MOCK_LAT
        assert response.json()["lon"] == MOCK_LON

    @pytest.mark.anyio
    async def test_get_location_by_coordinates_returns_404_when_not_found(
        self, async_client, auth_headers
    ):
        # Nothing inserted — DB is empty
        response = await async_client.get(
            "/api/v1/locations/locations/by-coordinates/",
            params={"lat": MOCK_LAT, "lon": MOCK_LON},
            headers=auth_headers,
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_location_by_coordinates_returns_403_without_auth(
        self, async_client
    ):
        response = await async_client.get(
            "/api/v1/locations/locations/by-coordinates/",
            params={"lat": MOCK_LAT, "lon": MOCK_LON},
        )

        assert response.status_code == 403


    @pytest.mark.skip(
        reason="Uses MongoDB $near geospatial query — not supported by mongomock. "
               "Requires a real MongoDB instance to test meaningfully."
    )
    async def test_check_location_exists_in_radius(self):
        pass

    @pytest.mark.anyio
    async def test_add_locations_returns_200_and_inserts(
        self, async_client, auth_headers
    ):
        payload = {
            "locations": [{"name": "Farm A", "lat": MOCK_LAT, "lon": MOCK_LON}]
        }

        with patch(
            "src.api.api_v1.endpoints.locations.fetch_and_cache_last_month",
            new_callable=AsyncMock
        ):
            response = await async_client.post(
                "/api/v1/locations/locations/",
                json=payload,
                headers=auth_headers,
            )

        assert response.status_code == 200
        # Verify it actually landed in the DB
        docs = await CachedLocation.find_all().to_list()
        assert len(docs) == 1
        assert docs[0].name == "Farm A"

    @pytest.mark.anyio
    async def test_add_locations_skips_existing_location(
        self, async_client, auth_headers, mock_location
    ):
        await self._insert_location("Farm A", location=mock_location)

        payload = {
            "locations": [{"name": "Farm A", "lat": MOCK_LAT, "lon": MOCK_LON}]
        }

        with patch(
            "src.api.api_v1.endpoints.locations.fetch_and_cache_last_month",
            new_callable=AsyncMock
        ):
            response = await async_client.post(
                "/api/v1/locations/locations/",
                json=payload,
                headers=auth_headers,
            )

        assert response.status_code == 200
        # Still only one document — duplicate was skipped
        docs = await CachedLocation.find_all().to_list()
        assert len(docs) == 1

    @pytest.mark.anyio
    async def test_add_locations_returns_403_without_auth(self, async_client):
        payload = {
            "locations": [{"name": "Farm A", "lat": MOCK_LAT, "lon": MOCK_LON}]
        }
        response = await async_client.post("/api/v1/locations/locations/", json=payload)
        assert response.status_code == 403

    @pytest.mark.skip(
        reason="Uses dao.find_location_nearby which relies on MongoDB $near "
               "geospatial query — not supported by mongomock."
    )
    async def test_add_unique_locations(self):
        pass

    @pytest.mark.anyio
    async def test_delete_location_returns_200(
        self, async_client, auth_headers, mock_location
    ):
        doc = await self._insert_location(location=mock_location)

        with patch(
            "src.api.api_v1.endpoints.locations.scheduler"
        ) as mock_scheduler:
            mock_scheduler.get_job.return_value = None
            response = await async_client.delete(
                f"/api/v1/locations/locations/{doc.id}/",
                headers=auth_headers,
            )

        assert response.status_code == 200
        # Verify it was actually removed from the DB
        remaining = await CachedLocation.find_all().to_list()
        assert len(remaining) == 0


    @pytest.mark.anyio
    async def test_delete_location_returns_403_without_auth(self, async_client):
        response = await async_client.delete("/api/v1/locations/locations/some-id/")
        assert response.status_code == 403