import pytest


@pytest.fixture()
def server_type_response():
    return {
        "server_type": {
            "id": 1,
            "name": "cx11",
            "description": "CX11",
            "cores": 1,
            "memory": 1,
            "disk": 25,
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
            "storage_type": "local",
            "cpu_type": "shared",
        }
    }


@pytest.fixture()
def two_server_types_response():
    return {
        "server_types": [
            {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
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
                "storage_type": "local",
                "cpu_type": "shared",
            },
            {
                "id": 2,
                "name": "cx21",
                "description": "CX21",
                "cores": 2,
                "memory": 4.0,
                "disk": 40,
                "prices": [
                    {
                        "location": "fsn1",
                        "price_hourly": {
                            "net": "0.0080000000",
                            "gross": "0.0095200000000000",
                        },
                        "price_monthly": {
                            "net": "4.9000000000",
                            "gross": "5.8310000000000000",
                        },
                    },
                    {
                        "location": "nbg1",
                        "price_hourly": {
                            "net": "0.0080000000",
                            "gross": "0.0095200000000000",
                        },
                        "price_monthly": {
                            "net": "4.9000000000",
                            "gross": "5.8310000000000000",
                        },
                    },
                ],
                "storage_type": "local",
                "cpu_type": "shared",
            },
        ]
    }


@pytest.fixture()
def one_server_types_response():
    return {
        "server_types": [
            {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
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
                "storage_type": "local",
                "cpu_type": "shared",
            }
        ]
    }
