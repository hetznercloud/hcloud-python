from __future__ import annotations

import pytest


@pytest.fixture()
def load_balancer_type_response():
    return {
        "load_balancer_type": {
            "id": 1,
            "name": "LB11",
            "description": "LB11",
            "max_connections": 1,
            "max_services": 1,
            "max_targets": 1,
            "max_assigned_certificates": 1,
            "deprecated": None,
            "prices": [
                {
                    "location": "fsn1",
                    "price_hourly": {
                        "net": "1.0000000000",
                        "gross": "1.1900000000000000",
                    },
                    "price_monthly": {
                        "net": "1.0000000000",
                        "gross": "1.1900000000000000",
                    },
                }
            ],
        }
    }


@pytest.fixture()
def two_load_balancer_types_response():
    return {
        "load_balancer_types": [
            {
                "id": 1,
                "name": "LB11",
                "description": "LB11D",
                "max_connections": 1,
                "max_services": 1,
                "max_targets": 1,
                "max_assigned_certificates": 1,
                "deprecated": None,
                "prices": [
                    {
                        "location": "fsn1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            },
            {
                "id": 2,
                "name": "LB21",
                "description": "LB21D",
                "max_connections": 2,
                "max_services": 2,
                "max_targets": 2,
                "max_assigned_certificates": 2,
                "deprecated": None,
                "prices": [
                    {
                        "location": "fsn1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            },
        ]
    }


@pytest.fixture()
def one_load_balancer_types_response():
    return {
        "load_balancer_types": [
            {
                "id": 2,
                "name": "LB21",
                "description": "LB21D",
                "max_connections": 2,
                "max_services": 2,
                "max_targets": 2,
                "max_assigned_certificates": 2,
                "deprecated": None,
                "prices": [
                    {
                        "location": "fsn1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            }
        ]
    }
