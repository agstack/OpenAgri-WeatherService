from unittest.mock import AsyncMock
from fastapi import FastAPI
import pytest
import mongomock
from httpx import AsyncClient

from src.core.dao import Dao
from src.main import create_app
from src.routes import router


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def app():
    _app = create_app()
    _app.include_router(router)

    # Mock the MongoDB client
    mongodb_client = mongomock.MongoClient()
    mongodb = mongodb_client["test_database"]
    _app.dao = Dao(mongodb_client)

    mock = AsyncMock()
    mock.get_forecast5day.return_value = {"forecast": "mocked_data"}
    mock.get_interoperable_forecast5day.return_value = {"forecast": "mocked_data"}
    _app.weather_app = mock

    yield _app


@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
