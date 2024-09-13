import logging

from fastapi import APIRouter, Request, HTTPException


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/api/data/forecast5")
async def get_weather_forecast5days(request: Request, lat: float, lon: float):
    try:
        result = await request.app.weather_app.get_weather_forecast5days(lat, lon)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)
    else:
      return result


@router.get("/api/linkeddata/forecast5")
async def get_weather_forecast5days_ld(request: Request, lat: float, lon: float):
    try:
        result = await request.app.weather_app.get_weather_forecast5days_ld(lat, lon)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
      return result


@router.get("/api/data/weather")
async def get_weather(request: Request, lat: float, lon: float):
    try:
        result = await request.app.weather_app.get_weather(lat, lon)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
      return result


@router.get("/api/data/thi")
async def get_thi(request: Request, lat: float, lon: float):
    try:
        result = await request.app.weather_app.get_thi(lat, lon)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)
    else:
      return result