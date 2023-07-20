from __future__ import annotations

import pytest


@pytest.fixture()
def response_create_placement_group():
    return {
        "placement_group": {
            "created": "2019-01-08T12:10:00+00:00",
            "id": 897,
            "labels": {"key": "value"},
            "name": "my Placement Group",
            "servers": [],
            "type": "spread",
        }
    }


@pytest.fixture()
def one_placement_group_response():
    return {
        "placement_groups": [
            {
                "created": "2019-01-08T12:10:00+00:00",
                "id": 897,
                "labels": {"key": "value"},
                "name": "my Placement Group",
                "servers": [4711, 4712],
                "type": "spread",
            }
        ]
    }


@pytest.fixture()
def two_placement_groups_response():
    return {
        "placement_groups": [
            {
                "created": "2019-01-08T12:10:00+00:00",
                "id": 897,
                "labels": {"key": "value"},
                "name": "my Placement Group",
                "servers": [4711, 4712],
                "type": "spread",
            },
            {
                "created": "2019-01-08T12:10:00+00:00",
                "id": 898,
                "labels": {"key": "value"},
                "name": "my Placement Group",
                "servers": [4713, 4714, 4715],
                "type": "spread",
            },
        ]
    }


@pytest.fixture()
def placement_group_response():
    return {
        "placement_group": {
            "created": "2019-01-08T12:10:00+00:00",
            "id": 897,
            "labels": {"key": "value"},
            "name": "my Placement Group",
            "servers": [4711, 4712],
            "type": "spread",
        }
    }
