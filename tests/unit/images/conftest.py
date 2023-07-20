from __future__ import annotations

import pytest


@pytest.fixture()
def image_response():
    return {
        "image": {
            "id": 4711,
            "type": "snapshot",
            "status": "available",
            "name": "ubuntu-20.04",
            "description": "Ubuntu 20.04 Standard 64 bit",
            "image_size": 2.3,
            "disk_size": 10,
            "created": "2016-01-30T23:50+00:00",
            "created_from": {"id": 1, "name": "Server"},
            "bound_to": 1,
            "os_flavor": "ubuntu",
            "os_version": "16.04",
            "architecture": "x86",
            "rapid_deploy": False,
            "protection": {"delete": False},
            "deprecated": "2018-02-28T00:00:00+00:00",
            "labels": {},
        }
    }


@pytest.fixture()
def two_images_response():
    return {
        "images": [
            {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "architecture": "x86",
                "rapid_deploy": False,
                "protection": {"delete": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
            {
                "id": 4712,
                "type": "system",
                "status": "available",
                "name": "ubuntu-18.10",
                "description": "Ubuntu 18.10 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "architecture": "x86",
                "rapid_deploy": False,
                "protection": {"delete": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
        ]
    }


@pytest.fixture()
def one_images_response():
    return {
        "images": [
            {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "architecture": "x86",
                "rapid_deploy": False,
                "protection": {"delete": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            }
        ]
    }


@pytest.fixture()
def response_update_image():
    return {
        "image": {
            "id": 4711,
            "type": "snapshot",
            "status": "available",
            "name": None,
            "description": "My new Image description",
            "image_size": 2.3,
            "disk_size": 10,
            "created": "2016-01-30T23:50+00:00",
            "created_from": {"id": 1, "name": "Server"},
            "bound_to": None,
            "os_flavor": "ubuntu",
            "os_version": "16.04",
            "architecture": "arm",
            "rapid_deploy": False,
            "protection": {"delete": False},
            "deprecated": "2018-02-28T00:00:00+00:00",
            "labels": {},
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "change_protection",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "image"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
