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
