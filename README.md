# Weather Service

## Description
Fast, reliable weather API providing 5-day forecasts, agricultural indicators like [Temperature-Humidity Index](https://www.pericoli.com/en/temperature-humidity-index-what-you-need-to-know-about-it/), UAV flight condition predictions, and spray condition forecasts. Built with FastAPI for high performance. Easy to integrate, deploy, and scale.


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

The application is served by default on `http://127.0.0.1:8000`

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

Get a complete list of the OpenApi specification compatible with [OCSM](OCSM.md) and [JSON](API.md)

## Swagger Live Docs
Use the [Online Swagger Editor](https://editor-next.swagger.io/?url=https://raw.githubusercontent.com/openagri-eu/weather-service/refs/heads/doc/document-api/openapi.yml) to visualise the current API specification and documentation.

## Contribute

Please contanct the repository maintainer.

## License

[European Union Public Licence](LICENSE)







