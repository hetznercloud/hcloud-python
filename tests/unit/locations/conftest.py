from __future__ import annotations

import pytest


@pytest.fixture()
def location_response():
    return {
        "location": {
            "id": 1,
            "name": "fsn1",
            "description": "Falkenstein DC Park 1",
            "country": "DE",
            "city": "Falkenstein",
            "latitude": 50.47612,
            "longitude": 12.370071,
            "network_zone": "eu-central",
        }
    }


@pytest.fixture()
def two_locations_response():
    return {
        "locations": [
            {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
                "network_zone": "eu-central",
            },
            {
                "id": 2,
                "name": "nbg1",
                "description": "Nuremberg DC Park 1",
                "country": "DE",
                "city": "Nuremberg",
                "latitude": 49.452102,
                "longitude": 11.076665,
                "network_zone": "eu-central",
            },
        ]
    }


@pytest.fixture()
def one_locations_response():
    return {
        "locations": [
            {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
                "network_zone": "eu-central",
            }
        ]
    }
