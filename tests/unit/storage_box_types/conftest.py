from __future__ import annotations

import pytest


@pytest.fixture()
def storage_box_type1():
    return {
        "id": 42,
        "name": "bx11",
        "description": "BX11",
        "snapshot_limit": 10,
        "automatic_snapshot_limit": 10,
        "subaccounts_limit": 100,
        "size": 1099511627776,
        "prices": [
            {
                "location": "fsn1",
                "price_hourly": {"gross": "0.0051", "net": "0.0051"},
                "price_monthly": {"gross": "3.2000", "net": "3.2000"},
                "setup_fee": {"gross": "0.0000", "net": "0.0000"},
            }
        ],
        "deprecation": {
            "unavailable_after": "2023-09-01T00:00:00+00:00",
            "announced": "2023-06-01T00:00:00+00:00",
        },
    }


@pytest.fixture()
def storage_box_type2():
    return {
        "id": 43,
        "name": "bx21",
        "description": "BX21",
        "snapshot_limit": 20,
        "automatic_snapshot_limit": 20,
        "subaccounts_limit": 100,
        "size": 5497558138880,
        "prices": [
            {
                "location": "fsn1",
                "price_hourly": {"net": "1.0000", "gross": "1.1900"},
                "price_monthly": {"net": "1.0000", "gross": "1.1900"},
                "setup_fee": {"net": "1.0000", "gross": "1.1900"},
            }
        ],
        "deprecation": None,
    }
