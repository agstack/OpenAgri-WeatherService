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

**GET**
```
/api/linkeddata/forecast5?lat={latitude}&lon={longitude}
```

**GET**
```
/api/data/thi?lat={latitude}&lon={longitude}
```

**GET**
```
/api/linkeddata/thi?lat={latitude}&lon={longitude}
```

**GET**
```
/api/data/weather?lat={latitude}&lon={longitude}
```

Get a complete list of the OpenApi specification [here](API.md)

For more info please run the application and read `http://digi-agri-services.greensupplychain.eu:8000/docs`

## Contribute

Please contanct the repository maintainer.

## License

[European Union Public Licence](LICENSE)







