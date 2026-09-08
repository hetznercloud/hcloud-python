from __future__ import annotations

import pytest


@pytest.fixture()
def image1():
    return {
        "id": 45557056,
        "name": "debian-11",
        "architecture": "x86",
        "bound_to": None,
        "created": "2021-08-16T11:12:01Z",
        "created_from": None,
        "deleted": None,
        "deprecated": "2026-08-31T06:21:44Z",
        "description": "Debian 11",
        "disk_size": 5,
        "image_size": None,
        "labels": {},
        "os_flavor": "debian",
        "os_version": "11",
        "protection": {
            "delete": False,
        },
        "rapid_deploy": True,
        "status": "available",
        "type": "system",
    }


@pytest.fixture()
def image2():
    return {
        "id": 429564329,
        "name": None,
        "architecture": "x86",
        "bound_to": 159969127,
        "created": "2026-09-08T13:44:08Z",
        "created_from": {
            "id": 159969127,
            "name": "server1",
        },
        "deleted": None,
        "deprecated": None,
        "description": "snapshot 2026-09-08T13:44:08Z",
        "disk_size": 80,
        "image_size": 0.7237785009765625,
        "labels": {
            "key": "value",
        },
        "os_flavor": "debian",
        "os_version": "13",
        "protection": {
            "delete": True,
        },
        "rapid_deploy": False,
        "status": "available",
        "type": "snapshot",
    }
