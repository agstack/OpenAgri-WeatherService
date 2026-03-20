"""
Pytest configuration and shared fixtures for all tests.
This file is automatically loaded by pytest.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import jwt
from beanie import Document, init_beanie
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient

import src.utils as utils
from src.api.api import data_router
from src.api.api_v1.api import api_router
from src.core import config
from src.core.dao import Dao
from src.external_services.openweathermap import OpenWeatherMap
from src.main import create_app
from src.models.uav import UAVModel
from src.schemas.uav import (FlightForecastListResponse,
                             FlightStatusForecastResponse)

# Configure pytest-asyncio
@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests"""
    return "asyncio"



@pytest.fixture
async def openweathermap_srv():

    dao_mock = AsyncMock()
    owm_srv = OpenWeatherMap()
    owm_srv.setup_dao(dao_mock)
    yield owm_srv


@pytest.fixture
async def app(openweathermap_srv):
    _app = create_app()
    _app.include_router(data_router)
    _app.include_router(api_router, prefix="/api/v1")

    # Mock the MongoDB client
    mongodb_client = AsyncMongoMockClient()
    mongodb = mongodb_client["test_database"]
    _app.dao = Dao(mongodb_client)
    await init_beanie(
        database=mongodb,
        document_models=utils.load_classes("**/models/**.py", (Document,)),
    )

    _app.weather_app = openweathermap_srv

    yield _app


@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def jwt_token():
    """Generate a valid JWT token for testing."""
    payload = {
        "sub": "test_user",
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token valid for 1 hour
        "roles": ["user"],  # Include any necessary claims
    }
    token = jwt.encode(payload, config.KEY, algorithm=config.ALGORITHM)
    return token

@pytest.fixture
def auth_headers(jwt_token):
    return {"Authorization": f"Bearer {jwt_token}"}

@pytest.fixture
def mock_uav(app):
    return UAVModel(
        model="DJI",
        manufacturer="MANU",
        max_wind_speed=10.0,
        min_operating_temp=-10.0,
        max_operating_temp=40.0,
        precipitation_tolerance=42.0,
    )




@pytest.fixture
def mock_owm_current_weather_response():
    """
    Moved here from TestOpenWeatherMapApi so that it can be shared
    """
    return {
        "coord": {"lon": -74.0060, "lat": 40.7128},
        "weather": [
            {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
        ],
        "main": {
            "temp": 25.5,
            "feels_like": 26.2,
            "temp_min": 23.0,
            "temp_max": 28.0,
            "pressure": 1013,
            "humidity": 60,
            "sea_level": 1013,
            "grnd_level": 1010,
        },
        "wind": {"speed": 5.2, "deg": 180, "gust": 7.8},
        "clouds": {"all": 0},
        "dt": 1640995200,
        "sys": {"country": "US"},
        "timezone": -18000,
        "id": 5128581,
        "name": "New York",
        "cod": 200,
    }

@pytest.fixture
def mock_location():
    return {"type": "Point", "coordinates": [-74.0060, 40.7128]}


@pytest.fixture
def mock_flight_response():
    """Mock flight forecast response"""
    return FlightForecastListResponse(
        forecasts=[
            FlightStatusForecastResponse(
                timestamp=datetime.utcnow().isoformat(),
                uavmodel="DJI",
                status="SAFE",
                weather_source="OpenWeatherMap",
                weather_params={"temp": 10, "wind": 5, "precipitation": 0.1},
                location={"type": "Point", "coordinates": [52.0, 13.0]},
            )
        ]
    )

# Configuration for pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
