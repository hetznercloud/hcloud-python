from __future__ import annotations

import pytest


@pytest.fixture()
def datacenter_response():
    return {
        "datacenter": {
            "id": 1,
            "name": "fsn1-dc8",
            "description": "Falkenstein 1 DC 8",
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "server_types": {
                "supported": [1, 2, 3],
                "available": [1, 2, 3],
                "available_for_migration": [1, 2, 3],
            },
        }
    }


@pytest.fixture()
def two_datacenters_response():
    return {
        "datacenters": [
            {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
            {
                "id": 2,
                "name": "nbg1-dc3",
                "description": "Nuremberg 1 DC 3",
                "location": {
                    "id": 2,
                    "name": "nbg1",
                    "description": "Nuremberg DC Park 1",
                    "country": "DE",
                    "city": "Nuremberg",
                    "latitude": 49.452102,
                    "longitude": 11.076665,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
        ],
        "recommendation": 1,
    }


@pytest.fixture()
def one_datacenters_response():
    return {
        "datacenters": [
            {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            }
        ],
        "recommendation": 1,
    }
