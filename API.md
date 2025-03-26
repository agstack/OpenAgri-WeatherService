## OpenApi Schema

**GET**
```
/api/data/forecast5
```
**Query params**
- lat: float
- lon: float

**Response**
```
[
  {
    "value": 14.59,
    "timestamp": "2024-11-01T09:00:00+00:00",
    "source": "openweathermaps",
    "spatial_entity": {
      "location": {
        "coordinates": [
          43.22,
          66.33
        ]
      }
    },
    "measurement_type": "ambient_temperature"
  },
  {
    "value": 42,
    "timestamp": "2024-11-01T09:00:00+00:00",
    "source": "openweathermaps",
    "spatial_entity": {
      "location": {
        "coordinates": [
          43.22,
          66.33
        ]
      }
    },
    "measurement_type": "ambient_humidity"
  },
    ...
  ]
```

**GET**
```
/api/data/thi
```
**Query params**
- lat: float
- lon: float

**Response**
```
{
  "spatial_entity": {
    "location": {
      "coordinates": [
        39.1436719,
        27.40518186
      ]
    }
  },
  "thi": 67.84
}

```

**GET**
```
/api/data/weather
```
**Query params**
- lat: float
- lon: float

**Response**
```
{
  "spatial_entity": {
    "location": {
      "coordinates": [
        54.7665,
        12.5544
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
      "temp": 13.39,
      "pressure": 1014,
      "humidity": 91
    },
    "wind": {
      "speed": 14.55
    },
    "dt": 1730449395
  }
}
```

**GET**
```
/api/data/flight_forecast5/{uavmodel}
```
**Input params**
- uavmodel: string

**Query params**
- lat: float
- lon: float

**Response**
```
{
  "forecasts": [
    {
      "timestamp": "2025-03-05T15:00:00",
      "uavmodel": "Mavic Pro",
      "status": "OK",
      "weather_source": "OpenWeatherMap",
      "location": {
        "_id": "295b1106-32ac-445e-bb89-c93ede238b60",
        "type": "Point",
        "coordinates": [
          45.4343,
          32.343434
        ]
      },
      "weather_params": {
        "temp": 7.38,
        "wind": 6.14,
        "precipitation": 0
      }
    },
    {
      "timestamp": "2025-03-05T15:00:00",
      "uavmodel": "Mavic Pro Platinum",
      "status": "OK",
      "weather_source": "OpenWeatherMap",
      "location": {
        "_id": "295b1106-32ac-445e-bb89-c93ede238b60",
        "type": "Point",
        "coordinates": [
          45.4343,
          32.343434
        ]
      },
      "weather_params": {
        "temp": 7.38,
        "wind": 6.14,
        "precipitation": 0
      }
    },
...
    {
      "timestamp": "2025-03-10T12:00:00",
      "uavmodel": "Zip",
      "status": "OK",
      "weather_source": "OpenWeatherMap",
      "location": {
        "_id": "295b1106-32ac-445e-bb89-c93ede238b60",
        "type": "Point",
        "coordinates": [
          45.4343,
          32.343434
        ]
      },
      "weather_params": {
        "temp": 7.3,
        "wind": 3,
        "precipitation": 0
      }
    }
  ]
}
```

**GET**
```
/api/data/flight_forecast5
```

**Query params**
- lat: float
- lon: float
- uavmodels: Optional list of UAV models to include in the forecast (eg. Mavic Pro)
- status_filter: Optional list of status conditions to filter results (eg. OK, NOT OK, MARGINAL)

**Response**
```
{
  "forecasts": [
    {
      "timestamp": "2025-03-05T15:00:00",
      "uavmodel": "Mavic Pro",
      "status": "OK",
      "weather_source": "OpenWeatherMap",
      "location": {
        "_id": "295b1106-32ac-445e-bb89-c93ede238b60",
        "type": "Point",
        "coordinates": [
          45.4343,
          32.343434
        ]
      },
      "weather_params": {
        "temp": 7.38,
        "wind": 6.14,
        "precipitation": 0
      }
    },
...
    {
      "timestamp": "2025-03-05T15:00:00",
      "uavmodel": "Mavic Pro Platinum",
      "status": "OK",
      "weather_source": "OpenWeatherMap",
      "location": {
        "_id": "295b1106-32ac-445e-bb89-c93ede238b60",
        "type": "Point",
        "coordinates": [
          45.4343,
          32.343434
        ]
      },
      "weather_params": {
        "temp": 7.38,
        "wind": 6.14,
        "precipitation": 0
      }
    },
  ]
}
```
