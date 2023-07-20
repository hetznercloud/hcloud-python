from __future__ import annotations

import pytest


@pytest.fixture()
def floating_ip_response():
    return {
        "floating_ip": {
            "id": 4711,
            "description": "Web Frontend",
            "name": "Web Frontend",
            "created": "2016-01-30T23:50+00:00",
            "ip": "131.232.99.1",
            "type": "ipv4",
            "server": 42,
            "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
            "home_location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "blocked": False,
            "protection": {"delete": False},
            "labels": {},
        }
    }


@pytest.fixture()
def one_floating_ips_response():
    return {
        "floating_ips": [
            {
                "id": 4711,
                "description": "Web Frontend",
                "name": "Web Frontend",
                "created": "2016-01-30T23:50+00:00",
                "ip": "131.232.99.1",
                "type": "ipv4",
                "server": 42,
                "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                "home_location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "blocked": False,
                "protection": {"delete": False},
                "labels": {},
            }
        ]
    }


@pytest.fixture()
def two_floating_ips_response():
    return {
        "floating_ips": [
            {
                "id": 4711,
                "description": "Web Frontend",
                "name": "Web Frontend",
                "created": "2016-01-30T23:50+00:00",
                "ip": "131.232.99.1",
                "type": "ipv4",
                "server": 42,
                "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                "home_location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "blocked": False,
                "protection": {"delete": False},
                "labels": {},
            },
            {
                "id": 4712,
                "description": "Web Backend",
                "name": "Web Backend",
                "created": "2016-01-30T23:50+00:00",
                "ip": "131.232.99.2",
                "type": "ipv4",
                "server": 42,
                "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                "home_location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "blocked": False,
                "protection": {"delete": False},
                "labels": {},
            },
        ]
    }


@pytest.fixture()
def floating_ip_create_response():
    return {
        "floating_ip": {
            "id": 4711,
            "description": "Web Frontend",
            "name": "Web Frontend",
            "created": "2016-01-30T23:50+00:00",
            "ip": "131.232.99.1",
            "type": "ipv4",
            "server": 42,
            "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
            "home_location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "blocked": False,
            "protection": {"delete": False},
            "labels": {},
        },
        "action": {
            "id": 13,
            "command": "assign_floating_ip",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
    }


@pytest.fixture()
def response_update_floating_ip():
    return {
        "floating_ip": {
            "id": 4711,
            "description": "New description",
            "name": "New name",
            "created": "2016-01-30T23:50+00:00",
            "ip": "131.232.99.1",
            "type": "ipv4",
            "server": 42,
            "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
            "home_location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "blocked": False,
            "protection": {"delete": False},
            "labels": {},
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "assign_floating_ip",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
