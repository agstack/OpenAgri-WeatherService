# Weather Service

[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL%201.2-blue.svg)](./LICENSE)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen)
[![Last commit](https://img.shields.io/github/last-commit/farmOS/farmOS.svg?style=flat)](https://github.com/agstack/openagri-weatherservice/commits)


Fast, reliable weather API with 5-day forecasts, agricultural indicators, UAV flight condition predictions, and spray condition forecasts.  
Built with [FastAPI](https://fastapi.tiangolo.com/) for high performance and easy integration.

**IMPORTANT**: This project is in an early stage. Some parts are stable, others need refactoring. We welcome contributors who want to help improve tests, documentation, and code quality.

---

## About

This service was created in the context of the [OpenAgri project](https://horizon-openagri.eu/), funded by the EU’s Horizon Europe research and innovation programme (Grant Agreement no. 101134083).

The Weather Service provides:

- **Forecasts** – 5-day forecasts in JSON and JSON-LD (OCSM) formats  
- **Current weather conditions** – temperature, humidity, wind, sky conditions  
- **Agricultural indicators** – Temperature-Humidity Index (THI)  
- **UAV flight forecasts** – 5-day predictions for UAV flight conditions (by model, filterable)  
- **Spray condition forecasts** – support for agricultural spraying planning  
- **Historical weather API** – daily and hourly values. You can find more info [here](history.md)
- **Offline support** – cache last month’s history for specific locations  
- **Containerized builds** – multi-arch Docker images (AMD64 and ARM64)  

---

## Roadmap

High-level next steps for the Weather Service:

- [ ] Connect with local weather stations for improved ground-truth data  
- [ ] Integrate with additional 3rd party weather APIs  
- [ ] Enhance accuracy of weather, UAV, and spray forecasts by combining multiple data sources  

---

## Quickstart

### Requirements

- `git`
- `docker`
- `docker-compose`

### Installation

## Clone repository:

```bash
git clone https://github.com/openagri-eu/OpenAgri-WeatherService.git
cd OpenAgri-WeatherService
cp env.example .env
```
You will then need to grab an api key for OpenWeatherMap API

## Getting an OpenWeather API Key

Some features of Weather Service use the [OpenWeather API](https://openweathermap.org/api).  
You’ll need your own API key to enable those calls.

1. Create a free account at [openweathermap.org](https://home.openweathermap.org/users/sign_up).
2. After signing up, go to your [API keys page](https://home.openweathermap.org/api_keys).
3. Copy the **default key** or generate a new one.
4. Add it to your `.env` file:
   ```env
   WEATHER_SRV_OPENWEATHERMAP_API_KEY=your-api-key-here
   ```
## Build & Run the service

```bash
docker compose up
```

By default, the API documentation is available at:

http://127.0.0.1:8010/docs

To build local docker image:
```bash
docker compose up --build
```

## Authentication

All API endpoints require a JWT.

### Get a token
Request a token using the dev credentials:

```bash
curl -X 'POST' \
  'http://localhost:8010/api/v1/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=test&password=test&scope=&client_id=&client_secret='
```

**Response:**
```bash
{"jwt_token": "<JWT>"}
```

**Use the token**

Pass the token as a Bearer header:
```bash
TOKEN="<paste JWT here>"
curl -s "http://127.0.0.1:8010/api/data/weather/?lat=35.0&lon=33.23/?lat=35.0&lon=33.23" \
  -H "Authorization: Bearer $TOKEN"
```

Tip: In Swagger UI (/docs), click Authorize and paste `Bearer <JWT>`.

## API Overview

### Forecasts

- `GET /api/data/forecast5/?lat={lat}&lon={lon}` – 5-day forecast (3-hour intervals, JSON)  
- `GET /api/linkeddata/forecast5/?lat={lat}&lon={lon}` – 5-day forecast (JSON-LD/OCSM)  

### Temperature-Humidity Index (THI)

- `GET /api/data/thi/?lat={lat}&lon={lon}` – THI (JSON)  
- `GET /api/linkeddata/thi/?lat={lat}&lon={lon}` – THI (JSON-LD/OCSM)  

### UAV Flight Forecast

- `GET /api/data/flight_forecast5/{uavmodel}/?lat={lat}&lon={lon}` – 5-day UAV forecast (by model)  
- `GET /api/data/flight_forecast5/?lat={lat}&lon={lon}&uavmodels={model}&status_filter={status}` – 5-day UAV forecast (filterable)  

### Current Weather

- `GET /api/data/weather/?lat={lat}&lon={lon}` – Current conditions (JSON)

### Historical weather data

- `POST /api/v1/history/hourly/` - Hourly history
- `POST /api/v1/history/daily/` - Daily history

---

## Documentation

- Interactive API docs: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs) (Swagger UI)  
- Full OpenAPI specification (JSON + OCSM JSON-LD) available via endpoints  
- Use [Swagger Editor](https://editor.swagger.io/) to explore the API specification  

## Environment Variables

All The following can be set in a `.env` file or as system environment variables. They can also be found in the 
settings config file `src/core/config.py`. You can also check .env.example for getting skeleton of the env variables 
to get started with

### Database and Server settings

We use MongoDB for storing historical weather data. Also MongoDb default port to be exposed is `27017`.

- `WEATHER_SRV_DATABASE_URI` – Database connection URL (default: SQLite `mongodb://root:root@localhost:27017/`)
- `WEATHER_SRV_DATABASE_NAME` - Database name (default: `openagridb`)
- `WEATHER_SRV_HOST` – Host for the FastAPI server (default: `weathersrv`)
- `WEATHER_SRV_PORT` – Port for the FastAPI server (default: `8000`)

### Jwt and Security settings

Which are typical default values for development and testing. For production, 
you should change these to secure values and manage them safely. Gatekeeper for credentials is recommended.

- `JWT_SECRET_KEY` – Secret key for signing JWTs (default: `some-key`)
- `JWT_ALGORITHM` – Algorithm for JWT (default: `HS256`)
- `CRYPT_CONTEXT_SCHEMES` – Password hashing schemes (default: `bcrypt`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` – Token expiry in minutes (default: `240`)

- `GATEKEEPER_URL` – Gatekeeper service URL (default: ``)
- `WEATHER_SRV_GATEKEEPER_USER` – Gatekeeper username (default: ``)
- `WEATHER_SRV_GATEKEEPER_PASSWORD` – Gatekeeper password (default: ``)
- `CURRENT_WEATHER_DATA_CACHE_TIME` - Time interval between location data is cached in hours, (default: `1`)

### External API Keys

Api keys for 3rd party services, Which the Weather Service uses to fetch weather data. 
Create free accounts to get your own keys, or use Gatekeeper to manage them.

- `WEATHER_SRV_OPENWEATHERMAP_API_KEY` – OpenWeatherMap API key (required for some features)
- `HISTORY_WEATHER_PROVIDER` - Weather data provider for historical data (default: `openmeteo`)
- `GATEKEEPER_FARM_CALENDAR_API` - Gatekeeper Farm Calendar API key (default: `http://farmcalendar:8002/api/v1/`)

### FARM Calendar settings
Integrations to Farm calendar service for information on this visit 
[OpenAgri-FarmCalendar](https://github.com/agstack/OpenAgri-FarmCalendar),This service allows for manual recording of: 
farmers operations, farmers observations, parcels properties and recording of farms’ assets.

For the usage examples you can check the implementations in `src/schedular.py`, Which contains various schedules, 
and appropriate debug messages.

- `PUSH_THI_TO_FARMCALENDAR` - Boolean value to push data to farm calendar, (default: `True`)
- `PUSH_FLIGHT_FORECAST_TO_FARMCALENDAR` - Push or Schedule UAV forcast to calendar, (default: `False`)
- `PUSH_SPRAY_F_TO_FARMCALENDAR` - Push or Schedule spray forcast to calendar, (default: `False`)
- `INTERVAL_HOURS_THI_TO_FARMCALENDAR` - Interval in hours between schedules, (default: `8`)

### Testing and Misc

Variables related to testings, server and Debug.

- `LOGGING_LEVEL` - values can be `DEBUG` or `info` based on the testing level, (default: `INFO`)
- `EXTRA_ALLOWED_HOSTS` - Allowed hosts for api communication, (Default: `*`)
- `LOCATION_RADIUS_METERS`- The range from the current location to check the data for in meters, (default, `10000`)

---

## Example Requests

### Current Weather

```bash
curl "http://127.0.0.1:8010/api/data/weather?lat=35.2&lon=33.3"
```
**Sample response:**

```json
{
  "temperature": 28.5,
  "humidity": 62,
  "wind_speed": 4.2,
  "conditions": "Clear sky",
  "timestamp": "2025-09-18T12:00:00Z"
}
```

### 5-Day Forecast

```bash
curl "http://127.0.0.1:8010/api/data/forecast5?lat=35.2&lon=33.3"
```

### Daily history
```bash
curl -X POST "http://127.0.0.1:8010/api/v1/history/daily" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 35.0,
    "lon": 33.2,
    "start": "2025-07-01",
    "end": "2025-07-03",
    "variables": ["temperature_2m_max", "temperature_2m_min"],
    "radius_km": 10
  }'
```

## Contributing

We welcome first-time contributions!

See our [Contributing Guide](CONTRIBUTE.md)

You can also open an issue to discuss ideas.

Weather Service is part of OpenAgri project, building tools for agriculture & climate data. Your contribution helps farmers and researchers.

This project exists thanks to all the people who contribute.

<a href="https://github.com/agstack/OpenAgri-WeatherService/graphs/contributors">
<img src="https://avatars.githubusercontent.com/u/1727181?v=4&s=80" width="60px;" alt="@fedjo's Avatar"/><img src="https://avatars.githubusercontent.com/u/369058?v=4&s=80" width="60px;" alt="@arruda's Avatar"/><img src="https://avatars.githubusercontent.com/u/58622550?v=4&s=80" width="60px;" alt="@GuND0Wn151's Avatar"/><img src="https://avatars.githubusercontent.com/u/159937181?v=4&s=80" width="60px;" alt="@Vidushi2709's Avatar"/></a>

## License

This project is licensed under the European Union Public Licence (EUPL) v1.2.
See the [European Union Public Licence](LICENSE) file for details.

