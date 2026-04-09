from __future__ import annotations

import pytest


@pytest.fixture()
def primary_ip1():
    return {
        "id": 42,
        "name": "primary-ip1",
        "type": "ipv4",
        "ip": "131.232.99.1",
        "assignee_id": 17,
        "assignee_type": "server",
        "auto_delete": True,
        "blocked": False,
        "datacenter": {
            "id": 4,
            "name": "fsn1-dc14",
        },
        "location": {
            "id": 1,
            "name": "fsn1",
        },
        "dns_ptr": [
            {"dns_ptr": "server.example.com", "ip": "131.232.99.1"},
        ],
        "labels": {"key": "value"},
        "protection": {"delete": False},
        "created": "2016-01-30T23:55:00Z",
    }


@pytest.fixture()
def primary_ip2():
    return {
        "id": 52,
        "name": "primary-ip2",
        "type": "ipv4",
        "ip": "131.232.99.2",
        "assignee_id": None,
        "assignee_type": "server",
        "auto_delete": True,
        "blocked": False,
        "datacenter": {
            "id": 4,
            "name": "fsn1-dc14",
        },
        "location": {
            "id": 1,
            "name": "fsn1",
        },
        "dns_ptr": [
            {"dns_ptr": "server.example.com", "ip": "131.232.99.1"},
        ],
        "labels": {"key": "value"},
        "protection": {"delete": False},
        "created": "2016-01-30T23:55:00Z",
    }
