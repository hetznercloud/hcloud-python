from __future__ import annotations

import pytest


@pytest.fixture()
def storage_box1():
    return {
        "id": 42,
        "name": "storage-box1",
        "created": "2025-01-30T23:55:00+00:00",
        "status": "active",
        "system": "FSN1-BX355",
        "server": "u1337.your-storagebox.de",
        "username": "u12345",
        "storage_box_type": {
            "id": 42,
            "name": "bx11",
        },
        "location": {
            "id": 1,
            "name": "fsn1",
        },
        "access_settings": {
            "reachable_externally": False,
            "samba_enabled": False,
            "ssh_enabled": False,
            "webdav_enabled": False,
            "zfs_enabled": False,
        },
        "snapshot_plan": {
            "max_snapshots": 20,
            "minute": 0,
            "hour": 7,
            "day_of_week": 7,
            "day_of_month": None,
        },
        "stats": {
            "size": 2342236717056,
            "size_data": 2102612983808,
            "size_snapshots": 239623733248,
        },
        "labels": {
            "key": "value",
        },
        "protection": {"delete": False},
    }


@pytest.fixture()
def storage_box2():
    return {
        "id": 43,
        "name": "storage-box2",
        "created": "2022-09-30T10:30:09.000Z",
        "status": "active",
        "system": "FSN1-BX355",
        "server": "u1337.your-storagebox.de",
        "username": "u12345",
        "storage_box_type": {
            "id": 1334,
            "name": "bx21",
        },
        "location": {
            "id": 1,
            "name": "fsn1",
        },
        "access_settings": {
            "webdav_enabled": False,
            "zfs_enabled": False,
            "samba_enabled": False,
            "ssh_enabled": True,
            "reachable_externally": True,
        },
        "snapshot_plan": {
            "max_snapshots": 20,
            "minute": 0,
            "hour": 7,
            "day_of_week": 7,
            "day_of_month": None,
        },
        "stats": {
            "size": 2342236717056,
            "size_data": 2102612983808,
            "size_snapshots": 239623733248,
        },
        "labels": {},
        "protection": {"delete": False},
    }


@pytest.fixture()
def storage_box_snapshot1():
    return {
        "id": 34,
        "name": "storage-box-snapshot1",
        "description": "",
        "is_automatic": False,
        "stats": {
            "size": 394957594,
            "size_filesystem": 3949572745,
        },
        "labels": {
            "key": "value",
        },
        "created": "2025-11-10T19:16:57Z",
        "storage_box": 42,
    }


@pytest.fixture()
def storage_box_snapshot2():
    return {
        "id": 35,
        "name": "storage-box-snapshot2",
        "description": "",
        "is_automatic": True,
        "stats": {
            "size": 0,
            "size_filesystem": 0,
        },
        "labels": {},
        "created": "2025-11-10T19:18:57Z",
        "storage_box": 42,
    }


@pytest.fixture()
def storage_box_subaccount1():
    return {
        "id": 45,
        "username": "u42-sub1",
        "server": "u42-sub1.your-storagebox.de",
        "home_directory": "tmp/",
        "description": "Required by foo",
        "access_settings": {
            "samba_enabled": False,
            "ssh_enabled": True,
            "webdav_enabled": False,
            "reachable_externally": True,
            "readonly": False,
        },
        "labels": {
            "key": "value",
        },
        "created": "2025-11-10T19:18:57Z",
        "storage_box": 42,
    }


@pytest.fixture()
def storage_box_subaccount2():
    return {
        "id": 46,
        "username": "u42-sub2",
        "server": "u42-sub2.your-storagebox.de",
        "home_directory": "backup/",
        "description": "",
        "access_settings": {
            "samba_enabled": False,
            "ssh_enabled": True,
            "webdav_enabled": False,
            "reachable_externally": True,
            "readonly": False,
        },
        "labels": {},
        "created": "2025-11-10T19:18:57Z",
        "storage_box": 42,
    }
