# Weather Service

🇪🇺 *This service was created in the context of OpenAgri project (https://horizon-openagri.eu/). OpenAgri has received funding from the EU’s Horizon Europe research and innovation programme under Grant Agreement no. 101134083.*

## Description
Fast, reliable weather API providing 5-day forecasts, agricultural indicators like
[Temperature-Humidity Index](https://www.pericoli.com/en/temperature-humidity-index-what-you-need-to-know-about-it/),
UAV flight condition predictions, and spray condition forecasts. Built with FastAPI for high performance.
Easy to integrate, deploy, and scale.


Project is fully functional, compatible with Python 3.12.
Is built using [FastAPI](https://fastapi.tiangolo.com/) framework and served with [Uvicorn](https://www.uvicorn.org).

The application is containerized using Docker. To install it please firstly install `docker`

You can follow [this guide](https://docs.docker.com/engine/install/ubuntu/) to install `docker` on Ubuntu.

## Requirements
- git
- docker
- docker-compose

## Installation
After installing `docker` you can simply run

```
docker compose up --build
```

to run the application.

The application is served by default on `http://127.0.0.1:8000`

## Documentation

**GET**
```
/api/data/forecast5?lat={latitude}&lon={longitude}
```
Retrieves a 5-day weather forecast with 3-hour intervals for a specific location. Response is in standard JSON format

**GET**
```
/api/linkeddata/forecast5?lat={latitude}&lon={longitude}
```
Retrieves the same 5-day weather forecast with 3-hour intervals, but returns data in OCSM JSON-LD format

**GET**
```
/api/data/thi?lat={latitude}&lon={longitude}
```
Provides the Temperature Humidity Index for a specific location in standard JSON format

**GET**
```
/api/linkeddata/thi?lat={latitude}&lon={longitude}
```
Provides the Temperature Humidity Index for a specific location in OCSM JSON-LD format

**GET**
```
/api/data/flight_forecast5/{uavmodel}?lat={latitude}&lon={longitude}
```
Retrieves a 5-day flight forecast with 3-hour intervals for a specific UAV model at the given location.
Response is in standard JSON format

**GET**
```
/api/data/flight_forecast5?lat={latitude}&lon={longitude}&uavmodels={model}&status_filter={status}
```
Retrieves a 5-day flight forecast with 3-hour intervals for UAVs at a specific location.
You can filter results by UAV model types and status conditions. Response is in standard JSON format


**GET**
```
/api/data/weather?lat={latitude}&lon={longitude}
```
Returns current weather conditions for a specific location in standard JSON format

Get a complete list of the OpenApi specification compatible with [OCSM](OCSM.md) and [JSON](API.md)

## Swagger Live Docs
Use the [Online Swagger Editor](https://editor-next.swagger.io/?url=https://raw.githubusercontent.com/agstack/openagri-weather-service/refs/heads/main/openapi.yml) to visualise the current API specification and documentation.

## Contribute

Please contanct the repository maintainer.

## License

[European Union Public Licence](LICENSE)







