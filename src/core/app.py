from functools import partial
import logging
import fastapi
from fastapi.openapi.utils import get_openapi

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document

from src.core import config
from src import utils
from src.core.dao import Dao
from src.routes import router
from src.external_services.openweathermap import OpenWeatherMap


logger = logging.getLogger(__name__)

class Application(fastapi.FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dao = self.setup_dao()
        self.weather_app = self.setup_weather_app()
        self.setup_routes()
        self.setup_openapi()


    def setup_dao(self):

        async def db_up(app: Application):
            await app.dao.db.admin.command('ping')
            logger.debug("You successfully connected to MongoDB!")
            # Init beanie with the Product document class
            await init_beanie(
                database=app.dao.db.get_database(config.DATABASE_NAME),
                document_models=utils.load_classes('**/models/**.py', (Document,))
            )

        async def db_down(app: Application):
            app.dao.db.close()
            logger.debug("Database closed!")

        self.add_event_handler(event_type="startup", func=partial(db_up, app=self))
        self.add_event_handler(event_type='shutdown', func=partial(db_down, app=self))
        return Dao(AsyncIOMotorClient(config.DATABASE_URI))

    def setup_routes(self):

        async def add_router(app: Application):
            logger.debug("Setup routes")
            app.include_router(router)
            logger.debug("Routes added!")

        self.add_event_handler(event_type="startup", func=partial(add_router, app=self))
        return


    def setup_weather_app(self):
        logger.debug("Setup connection with external weather service")

        async def add_dao(app: Application):
            app.weather_app.setup_dao(app.dao)

        self.add_event_handler(event_type="startup", func=partial(add_dao, app=self))
        return OpenWeatherMap()

    def setup_openapi(self):

        async def add_openapi_schema(app: Application):
            if app.openapi_schema:
                return
            openapi_schema = get_openapi(
                title="OpenAgri Weather service",
                version="2.5.0",
                summary="This is OpenAPI for OpenAgri Weather service",
                description="",
                routes=app.routes,
            )
            app.openapi_schema = openapi_schema

        self.add_event_handler(event_type="startup", func=partial(add_openapi_schema, app=self))
        return