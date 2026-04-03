from fastapi import APIRouter
from .endpoints import auth, locations, history, forecast


api_router = APIRouter()
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["forecast-hourly"])

