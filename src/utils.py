import base64
import csv
from datetime import datetime, timedelta, timezone
import functools
import glob
from importlib import import_module
import inspect
import logging
import os
import struct
import copy
import uuid


from fastapi import APIRouter
import httpx

from src.models.spray import SprayStatus
from src.models.uav import FlightStatus, UAVModel


logger = logging.getLogger(__name__)


def deepcopy_dict(d: dict) -> dict:
    return copy.deepcopy(d)


def extract_value_from_dict_path(d: dict, path: list):
    return functools.reduce(
                lambda elem, current_path: elem[current_path] if elem and current_path in elem else None,
                path,
                d
            )


# Convert UNIX timestamp in string in format HH:MM:SS
# Optionally select ISO8601 format string
def convert_timestamp_to_string(dt_timestamp, tz_offset, iso=False):
    tz = timezone(timedelta(seconds=tz_offset))
    dt_object =  datetime.fromtimestamp(dt_timestamp, tz=tz)

    if iso:
        return dt_object.isoformat()
    return dt_object.strftime("%H:%M:%S")


# List application routes
def list_routes_from_routers(routers: list[APIRouter]):
    routes = []
    for router in routers:
        for route in router.routes:
            if hasattr(route, "methods"):
                routes.append({"path": route.path, "methods": list(route.methods)})
    return routes


# Function to generate a UUID with a specific prefix
def generate_uuid(prefix, identifier=None):
    return f"urn:openagri:{prefix}:{identifier if identifier else uuid.uuid4()}"


async def http_get(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


## Temperature Humidity Index
# https://www.pericoli.com/en/temperature-humidity-index-what-you-need-to-know-about-it/

def calculate_thi(temperature: float, relative_humidity: float) -> float:
    relative_humidity = relative_humidity / 100 # Convert to % percentage
    thi = (0.8 * temperature) + (relative_humidity * (temperature - 14.4)) + 46.4
    return round(thi, 2)


def number_to_base32_string(num: float) -> str:
    '''
    Explanation:

    Struct Packing: struct.pack('>q', num) converts the integer number to a byte array in big-endian format using the >q format (signed long long, 8 bytes).
    Base32 Encoding: base64.b32encode encodes the byte array to a base-32 encoded bytes object.
    Decoding: .decode('utf-8') converts the bytes object to a string.
    Stripping Equals: .rstrip('=') removes any trailing equal signs used for padding in base-32 encoding.
    '''
    # Convert the number to a byte array
    byte_array = struct.pack('>q', num)  # Use '>q' for long long (8 bytes)
    
    # Encode the byte array using base32
    base32_encoded = base64.b32encode(byte_array).decode('utf-8').rstrip('=')
    
    return base32_encoded


def load_classes(pathname, base_classes):
    classes = []
    for path in glob.glob(pathname, recursive=True):
        module = import_module(os.path.splitext(path)[0].strip('./').replace('/', '.'))
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj not in base_classes and issubclass(obj, base_classes):
                classes.append(obj)

    return classes


# Reads the CSV file without pandas and inserts data into MongoDB
async def load_uavs_from_csv(csv_path: str):
    # Checks if data exists before inserting new records from CSV
    existing_count = await UAVModel.count()
    if existing_count > 0:
        logging.info(f"Skipping CSV import. {existing_count} uavs already exist in the database.")
        return

    uavs = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert data types where needed
            uav_data = {
                "model": row["Model"],
                "manufacturer": row["Manufacturer"],
                "min_operating_temp": float(row["Min. operating temp"]),
                "max_operating_temp": float(row["Max. operating temp"]),
                "max_wind_speed": float(row["Max. wind speed resistance"]),
                "precipitation_tolerance": float(row["Precipitation tolerance"]),
            }
            uavs.append(UAVModel(**uav_data))

    if uavs:
        await UAVModel.insert_many(uavs)
        logger.info(f"Inserted {len(uavs)} uav records into MongoDB.")
    else:
        logger.info("No records found in the CSV file.")


# Determines flight conditions based on uav specifications and weather data
async def evaluate_flight_conditions(uav: UAVModel, weather: dict) -> FlightStatus:
    temp = weather["temp"]
    wind = weather["wind"]
    precipitation = weather["precipitation"]

    if temp < uav.min_operating_temp or temp > uav.max_operating_temp:
        return FlightStatus.NOT_OK
    if wind > uav.max_wind_speed or precipitation > uav.precipitation_tolerance:
        return FlightStatus.NOT_OK
    if wind >= uav.max_wind_speed * 0.8 or precipitation > 0:
        return FlightStatus.MARGINALLY_OK
    
    return FlightStatus.OK

#   Evaluate spray conditions based on weather data
#   Determines the spray condition based on weather parameters.
#   Returns a tuple: (spray_condition, detailed_status_dict)
#
#   Parameters:
#   - temp: Temperature in Celsius
#   - wind: Wind speed in km/h
#   - precipitation: Precipitation in mm
#   - humidity: Relative humidity in percentage
#   - delta_t: Temperature difference in Celsius
#
#   Returns:
#   - tuple: (SprayStatus enum value, dictionary of individual parameter statuses)
#
def evaluate_spray_conditions(temp, wind, precipitation, humidity, delta_t):
    status = {}

    # Temperature Check
    if temp < 18:
        status["temperature_status"] = SprayStatus.OPTIMAL
    elif 18 <= temp <= 25:
        status["temperature_status"] = SprayStatus.MARGINAL
    else:
        status["temperature_status"] = SprayStatus.UNSUITABLE

    # Wind Speed Check
    if wind < 15:
        status["wind_status"] = SprayStatus.OPTIMAL
    elif 15 <= wind <= 25:
        status["wind_status"] = SprayStatus.MARGINAL
    else:
        status["wind_status"] = SprayStatus.UNSUITABLE

    # Precipitation Check
    if precipitation == 0:
        status["precipitation_status"] = SprayStatus.OPTIMAL
    elif 0 < precipitation <= 0.1:
        status["precipitation_status"] = SprayStatus.MARGINAL
    else:
        status["precipitation_status"] = SprayStatus.UNSUITABLE

    # Humidity Check
    if 60 <= humidity <= 85:
        status["humidity_status"] = SprayStatus.OPTIMAL
    elif 45 <= humidity < 60 or 85 < humidity <= 95:
        status["humidity_status"] = SprayStatus.MARGINAL
    else:
        status["humidity_status"] = SprayStatus.UNSUITABLE

    # Delta T Check
    if 2 <= delta_t <= 8:
        status["delta_t_status"] = SprayStatus.OPTIMAL
    elif 0 <= delta_t < 2 or 8 < delta_t <= 10:
        status["delta_t_status"] = SprayStatus.MARGINAL
    else:
        status["delta_t_status"] = SprayStatus.UNSUITABLE

    # Determine overall spray condition
    if SprayStatus.UNSUITABLE in status.values():
        spray_condition = SprayStatus.UNSUITABLE
    elif SprayStatus.MARGINAL in status.values():
        spray_condition = SprayStatus.MARGINAL
    else:
        spray_condition = SprayStatus.OPTIMAL

    return spray_condition, status

