from __future__ import annotations

import pytest


@pytest.fixture()
def network_response():
    return {
        "network": {
            "id": 1,
            "name": "mynet",
            "created": "2016-01-30T23:50:11+00:00",
            "ip_range": "10.0.0.0/16",
            "subnets": [
                {
                    "type": "cloud",
                    "ip_range": "10.0.1.0/24",
                    "network_zone": "eu-central",
                    "gateway": "10.0.0.1",
                },
                {
                    "type": "vswitch",
                    "ip_range": "10.0.3.0/24",
                    "network_zone": "eu-central",
                    "gateway": "10.0.3.1",
                },
            ],
            "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            "expose_routes_to_vswitch": False,
            "servers": [42],
            "protection": {"delete": False},
            "labels": {},
        }
    }


@pytest.fixture()
def two_networks_response():
    return {
        "networks": [
            {
                "id": 1,
                "name": "mynet",
                "created": "2016-01-30T23:50:11+00:00",
                "ip_range": "10.0.0.0/16",
                "subnets": [
                    {
                        "type": "cloud",
                        "ip_range": "10.0.1.0/24",
                        "network_zone": "eu-central",
                        "gateway": "10.0.0.1",
                    },
                    {
                        "type": "vswitch",
                        "ip_range": "10.0.3.0/24",
                        "network_zone": "eu-central",
                        "gateway": "10.0.3.1",
                    },
                ],
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
                "expose_routes_to_vswitch": False,
                "servers": [42],
                "protection": {"delete": False},
                "labels": {},
            },
            {
                "id": 2,
                "name": "myanothernet",
                "created": "2016-01-30T23:50:11+00:00",
                "ip_range": "12.0.0.0/8",
                "subnets": [
                    {
                        "type": "cloud",
                        "ip_range": "12.0.1.0/24",
                        "network_zone": "eu-central",
                        "gateway": "12.0.0.1",
                    }
                ],
                "routes": [{"destination": "12.100.1.0/24", "gateway": "12.0.1.1"}],
                "expose_routes_to_vswitch": False,
                "servers": [45],
                "protection": {"delete": False},
                "labels": {},
            },
        ]
    }


@pytest.fixture()
def one_network_response():
    return {
        "networks": [
            {
                "id": 1,
                "name": "mynet",
                "created": "2016-01-30T23:50:11+00:00",
                "ip_range": "10.0.0.0/16",
                "subnets": [
                    {
                        "type": "cloud",
                        "ip_range": "10.0.1.0/24",
                        "network_zone": "eu-central",
                        "gateway": "10.0.0.1",
                    },
                    {
                        "type": "vswitch",
                        "ip_range": "10.0.3.0/24",
                        "network_zone": "eu-central",
                        "gateway": "10.0.3.1",
                    },
                ],
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
                "expose_routes_to_vswitch": False,
                "servers": [42],
                "protection": {"delete": False},
                "labels": {},
            }
        ]
    }


@pytest.fixture()
def network_create_response():
    return {
        "network": {
            "id": 4711,
            "name": "mynet",
            "ip_range": "10.0.0.0/16",
            "subnets": [
                {
                    "type": "cloud",
                    "ip_range": "10.0.1.0/24",
                    "network_zone": "eu-central",
                    "gateway": "10.0.0.1",
                }
            ],
            "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            "expose_routes_to_vswitch": False,
            "servers": [42],
            "protection": {"delete": False},
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
        }
    }


@pytest.fixture()
def network_create_response_with_expose_routes_to_vswitch():
    return {
        "network": {
            "id": 4711,
            "name": "mynet",
            "ip_range": "10.0.0.0/16",
            "subnets": [
                {
                    "type": "cloud",
                    "ip_range": "10.0.1.0/24",
                    "network_zone": "eu-central",
                    "gateway": "10.0.0.1",
                }
            ],
            "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            "expose_routes_to_vswitch": True,
            "servers": [42],
            "protection": {"delete": False},
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
        }
    }


@pytest.fixture()
def response_update_network():
    return {
        "network": {
            "id": 4711,
            "name": "new-name",
            "ip_range": "10.0.0.0/16",
            "subnets": [
                {
                    "type": "cloud",
                    "ip_range": "10.0.1.0/24",
                    "network_zone": "eu-central",
                    "gateway": "10.0.0.1",
                }
            ],
            "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            "expose_routes_to_vswitch": True,
            "servers": [42],
            "protection": {"delete": False},
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "add_subnet",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 4711, "type": "network"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
