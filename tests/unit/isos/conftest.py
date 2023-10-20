from __future__ import annotations

import pytest


@pytest.fixture()
def iso_response():
    return {
        "iso": {
            "id": 4711,
            "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
            "description": "FreeBSD 11.0 x64",
            "type": "public",
            "architecture": "x86",
            "deprecated": "2018-02-28T00:00:00+00:00",
            "deprecation": {
                "announced": "2018-01-28T00:00:00+00:00",
                "unavailable_after": "2018-02-28T00:00:00+00:00",
            },
        }
    }


@pytest.fixture()
def two_isos_response():
    return {
        "isos": [
            {
                "id": 4711,
                "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
                "description": "FreeBSD 11.0 x64",
                "type": "public",
                "architecture": "x86",
                "deprecated": "2018-02-28T00:00:00+00:00",
                "deprecation": {
                    "announced": "2018-01-28T00:00:00+00:00",
                    "unavailable_after": "2018-02-28T00:00:00+00:00",
                },
            },
            {
                "id": 4712,
                "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
                "description": "FreeBSD 11.0 x64",
                "type": "public",
                "architecture": "x86",
                "deprecated": None,
            },
        ]
    }


@pytest.fixture()
def one_isos_response():
    return {
        "isos": [
            {
                "id": 4711,
                "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
                "description": "FreeBSD 11.0 x64",
                "type": "public",
                "architecture": "x86",
                "deprecated": "2018-02-28T00:00:00+00:00",
                "deprecation": {
                    "announced": "2018-01-28T00:00:00+00:00",
                    "unavailable_after": "2018-02-28T00:00:00+00:00",
                },
            }
        ]
    }
