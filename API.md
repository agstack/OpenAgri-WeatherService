## OpenApi Schema

**GET**
```
/api/data/forecast5?lat={latitude}&lon={longitude}
```
Example Response:
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
/api/linkeddata/forecast5?lat={latitude}&lon={longitude}
```
Example Response:
```
{
  "@context": [
    "https://w3id.org/ocsm/main-context.jsonld",
    {
      "qudt": "http://qudt.org/vocab/unit/",
      "cf": "https://vocab.nerc.ac.uk/standard_name/"
    }
  ],
  "@graph": [
    {
      "@id": "urn:openagri:weather:forecast:2024-11-01 09:00:00+00:00",
      "@type": [
        "ObservationCollection",
        "WeatherForecast"
      ],
      "description": "5-day weather forecast",
      "hasFeatureOfInterest": {
        "@id": "urn:openagri:weather:forecast:foi:59fd7deb-3cc3-47f1-a221-35dda01a9bab",
        "@type": [
          "FeatureOfInterest",
          "POI"
        ],
        "long": 55.8888,
        "lat": 33.88
      },
      "source": "openweathermaps",
      "resultTime": "2024-11-01T09:00:00+00:00",
      "phenomenonTime": "2024-11-01T09:00:00+00:00",
      "hasMember": [
        {
          "@id": "urn:openagri:weather:forecast:winddirection:51d5e2c1-8be0-47fe-89c8-19151adf45a8",
          "@type": "Observation",
          "observedProperty": "cf:wind_direction",
          "hasResult": {
            "@id": "urn:openagri:weather:forecast:winddirection:result:51d5e2c1-8be0-47fe-89c8-19151adf45a8",
            "@type": "Result",
            "numericValue": 8,
            "unit": "Degree"
          }
        }
      ]
    },
    {
      "@id": "urn:openagri:weather:forecast:2024-11-01 12:00:00+00:00",
      "@type": [
        "ObservationCollection",
        "WeatherForecast"
      ],
      "description": "5-day weather forecast",
      "hasFeatureOfInterest": {
        "@id": "urn:openagri:weather:forecast:foi:59fd7deb-3cc3-47f1-a221-35dda01a9bab",
        "@type": [
          "FeatureOfInterest",
          "POI"
        ],
        "long": 55.8888,
        "lat": 33.88
      },
      "source": "openweathermaps",
      "resultTime": "2024-11-01T12:00:00+00:00",
      "phenomenonTime": "2024-11-01T12:00:00+00:00",
      "hasMember": [
        {
          "@id": "urn:openagri:weather:forecast:winddirection:04fefaac-1abe-497d-a99d-86ead1ce8349",
          "@type": "Observation",
          "observedProperty": "cf:wind_direction",
          "hasResult": {
            "@id": "urn:openagri:weather:forecast:winddirection:result:04fefaac-1abe-497d-a99d-86ead1ce8349",
            "@type": "Result",
            "numericValue": 25,
            "unit": "Degree"
          }
        }
      ]
    },
    ...
  ]
}
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
/api/linkeddata/thi?lat={latitude}&lon={longitude}
```
Example Response:
```
{
  "@context": [
    "https://w3id.org/ocsm/main-context.jsonld",
    {
      "qudt": "http://qudt.org/vocab/unit/",
      "cf": "https://vocab.nerc.ac.uk/standard_name/"
    }
  ],
  "@graph": [
    {
      "@id": "urn:openagri:weather:data:1730449361",
      "@type": [
        "ObservationCollection"
      ],
      "description": "Temperature Humidity Index",
      "hasFeatureOfInterest": {
        "@id": "urn:openagri:weather:data:foi:4e8dedcc-da30-4b52-9c0c-faca069b7633",
        "@type": [
          "FeatureOfInterest",
          "POI"
        ],
        "long": 44.7678,
        "lat": 23.6652
      },
      "source": "openweathermaps",
      "resultTime": 1730449361,
      "phenomenonTime": 1730449361,
      "hasMember": [
        {
          "@id": "urn:openagri:weather:data:thi:2e5ff81a-298b-4504-bcfc-b3899a005933",
          "@type": "Observation",
          "observedProperty": "cf:temperature_humidity_index",
          "hasResult": {
            "@id": "urn:openagri:weather:data:thi:result:2e5ff81a-298b-4504-bcfc-b3899a005933",
            "@type": "Result",
            "numericValue": 71.06,
            "unit": null
          }
        }
      ]
    }
  ]
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