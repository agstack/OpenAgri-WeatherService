## OCSM Schema

**GET**
```
/api/linkeddata/forecast5
```
**Query params**
- lat: float
- lon: float

**Response**
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
/api/linkeddata/thi
```
**Query params**
- lat: float
- lon: float

**Response**
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