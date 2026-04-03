from datetime import datetime, timezone
import logging

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core import config
from src.models.history_data import CachedLocation
from src.services.jobs import update_sliding_window

scheduler = AsyncIOScheduler()


# Schedule THI tasks for each location
async def schedule_tasks(app: FastAPI):
    scheduler.remove_all_jobs()  # Clear old jobs

    for location_info in (await app.state.fc_client.fetch_locations()):
        lat, lon = location_info["lat"], location_info["lon"]
        farm, parcel = location_info["farm_name"], location_info["identifier"]
        if config.PUSH_THI_TO_FARMCALENDAR:
            scheduler.add_job(
                post_thi_task,
                "interval",
                hours=config.INTERVAL_THI_TO_FARMCALENDAR,
                next_run_time=datetime.now(timezone.utc),
                id=f"thi_task_{lat}_{lon}",
                replace_existing=True,
                args=[app, location_info]
            )
            logging.debug(f"THI scheduling for farm: {farm}, parcel: {parcel}")
        if config.PUSH_FLIGHT_FORECAST_TO_FARMCALENDAR:
            scheduler.add_job(
                post_flight_forecast,
                "interval",
                days=5,
                next_run_time=datetime.now(timezone.utc),
                id=f"flight_forecast_task_{lat}_{lon}",
                replace_existing=True,
                args=[app, location_info, app.state.uavmodels]
            )
            logging.debug(f"Scheduled UAV forecast task for farm: {farm}, parcel: {parcel}")
        if config.PUSH_SPRAY_F_TO_FARMCALENDAR:
            scheduler.add_job(
                post_spray_forecast,
                "interval",
                days=5,
                next_run_time=datetime.now(timezone.utc),
                id=f"spray_forecast_task_{lat}_{lon}",
                replace_existing=True,
                args=[app, location_info]
            )
            logging.debug(f"Scheduled spray conditions forecast task for farm: {farm}, parcel: {parcel}"    )

    locations = await CachedLocation.find_all().to_list()
    for loc in locations:
        lat, lon = loc.location["coordinates"][1], loc.location["coordinates"][0]
        scheduler.add_job(
            update_sliding_window,
            trigger="cron",
            hour=23,
            args=[lat, lon, config.OM_CACHE_VARIABLES],
            id=f"update_sliding_{lat}_{lon}",
            replace_existing=True,
        )
        logging.debug("Scheduled sliding window update for %s, %s", lat, lon)


# Post THI for a single location
async def post_thi_task(app, location_info):
    fc_client = app.state.fc_client
    farm, parcel = location_info["farm_name"], location_info["identifier"]
    logging.debug(f"Posting THI for {farm}, {parcel}")
    await fc_client.send_thi(location_info)

# Post flight forecast for a single location
async def post_flight_forecast(app, location_info, uavmodels):
    fc_client = app.state.fc_client
    farm, parcel = location_info["farm_name"], location_info["identifier"]
    logging.debug(f"Posting Flight forecast for models: {uavmodels} at location: ({farm}, {parcel})")
    await fc_client.send_flight_forecast(location_info, uavmodels)

# Post spray conditions forecast for a single location
async def post_spray_forecast(app, location_info):
    fc_client = app.state.fc_client
    farm, parcel = location_info["farm_name"], location_info["identifier"]
    logging.debug(f"Posting spray conditions forecast at location: ({farm}, {parcel})")
    await fc_client.send_spray_forecast(location_info)


# Fetch locations & update scheduler every 24 hours
async def refresh_locations_and_schedule(app):
    await app.state.fc_client.fetch_and_cache_locations()
    await schedule_tasks(app)

# Fetch machines & update scheduler every 24 hours
async def refresh_machines_and_schedule(app):
    await app.state.fc_client.fetch_and_cache_uavs()
    await schedule_tasks(app)



async def start_scheduler(app: FastAPI):

    await schedule_tasks(app)

    # Refresh locations and reschedule every 24 hours
    scheduler.add_job(refresh_locations_and_schedule, "interval", minutes=5, args=[app])
    # Refresh machines and reschedule every 24 hours
    scheduler.add_job(refresh_machines_and_schedule, "interval", minutes=5, args=[app])


    scheduler.start()
