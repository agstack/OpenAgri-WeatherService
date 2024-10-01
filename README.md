# Weather Service

## Description

This a simple service providing a 5-day weather forecast for a specific location. It also calculates critical agricultural indicators,
such as the Temperature-Humidity Index (THI). The service uses OpenWeatherMap API to extract necessary information.

THI is a combined metric used to assess heat stress in livestock, calculated using air temperature and relative humidity.
The THI formula is as follows:
```
THI = 0.8 * T + RH * (T - 14.4) + 46.4
```
Where:
**T** is the air temperature (in degrees Celsius)
**RH** is the relative humidity (as a percentage)


Project is fully functional, compatible with Python 3.12. Is built using [FastAPI](https://fastapi.tiangolo.com/) framework and served with [Uvicorn](https://www.uvicorn.org).

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

The application is served on `http://127.0.0.1:8000`

## Documentation

**GET**
```
/api/data/forecast5?lat={latitude}&lon={longitude}
```
Example Response:
```
[
  {
    "value": 22.53,
    "timestamp": "2024-10-01T12:00:00+00:00",
    "source": "openweathermaps",
    "spatial_entity": {
      "location": {
        "coordinates": [
          39.1436719643054,
          27.40518186700786
        ]
      }
    },
    "measurement_type": "ambient_temperature"
  },
  {
    "value": 38,
    "timestamp": "2024-10-01T12:00:00+00:00",
    "source": "openweathermaps",
    "spatial_entity": {
      "location": {
        "coordinates": [
          39.1436719643054,
          27.40518186700786
        ]
      }
    },
    "measurement_type": "ambient_humidity"
  }]
```
**GET**
```
/api/data/thi?lat={latitude}&lon={longitude}
```
Example Response:
```
{
  "spatial_entity": {
    "location": {
      "coordinates": [
        39.1436719643054,
        27.40518186700786
      ]
    }
  },
  "thi": 67.84
}

```
**GET**
```
/api/data/weather?lat={latitude}&lon={longitude}
```
Example Response:
```
{
  "spatial_entity": {
    "location": {
      "coordinates": [
        39.1436719643054,
        27.40518186700786
      ]
    }
  },
  "data": {
    "weather": [
      {
        "description": "clear sky"
      }
    ],
    "main": {
      "temp": 23.6,
      "pressure": 1011,
      "humidity": 35
    },
    "wind": {
      "speed": 3.78
    },
    "dt": 1727778917
  }
}

```

For more info please run the application and read `http://localhost:8000/docs`

## Contribute

Please contanct maintainer.

## License

[European Union Public Licence](LICENSE)







