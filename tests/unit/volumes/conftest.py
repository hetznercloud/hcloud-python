from __future__ import annotations

import pytest


@pytest.fixture()
def volume_response():
    return {
        "volume": {
            "id": 1,
            "created": "2016-01-30T23:50:11+00:00",
            "name": "database-storage",
            "server": 12,
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "size": 42,
            "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
            "protection": {"delete": False},
            "format": "xfs",
            "labels": {},
            "status": "available",
        }
    }


@pytest.fixture()
def two_volumes_response():
    return {
        "volumes": [
            {
                "id": 1,
                "created": "2016-01-30T23:50:11+00:00",
                "name": "database-storage",
                "server": 12,
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "size": 42,
                "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
                "protection": {"delete": False},
                "format": "xfs",
                "labels": {},
                "status": "available",
            },
            {
                "id": 2,
                "created": "2016-01-30T23:50:11+00:00",
                "name": "vault-storage",
                "server": 10,
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 2",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "size": 42,
                "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
                "protection": {"delete": False},
                "format": "xfs",
                "labels": {},
                "status": "available",
            },
        ]
    }


@pytest.fixture()
def one_volumes_response():
    return {
        "volumes": [
            {
                "id": 1,
                "created": "2016-01-30T23:50:11+00:00",
                "name": "database-storage",
                "server": 12,
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "size": 42,
                "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
                "protection": {"delete": False},
                "format": "xfs",
                "labels": {},
                "status": "available",
            }
        ]
    }


@pytest.fixture()
def volume_create_response():
    return {
        "volume": {
            "id": 4711,
            "created": "2016-01-30T23:50:11+00:00",
            "name": "database-storage",
            "server": 12,
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "size": 42,
            "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
            "protection": {"delete": False},
            "format": "xfs",
            "labels": {},
            "status": "available",
        },
        "action": {
            "id": 13,
            "command": "create_volume",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
        "next_actions": [
            {
                "id": 13,
                "command": "start_server",
                "status": "running",
                "progress": 0,
                "started": "2016-01-30T23:50+00:00",
                "finished": None,
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ],
    }


@pytest.fixture()
def response_update_volume():
    return {
        "volume": {
            "id": 4711,
            "created": "2016-01-30T23:50:11+00:00",
            "name": "new-name",
            "server": 12,
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
            },
            "format": "xfs",
            "size": 42,
            "linux_device": "/dev/disk/by-id/scsi-0HC_Volume_4711",
            "protection": {"delete": False},
            "labels": {},
            "status": "available",
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "attach_volume",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
