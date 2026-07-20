from __future__ import annotations

import pytest


@pytest.fixture()
def load_balancer_type1():
    return {
        "id": 1,
        "name": "lb11",
        "description": "LB11",
        "max_connections": 10000,
        "max_services": 5,
        "max_targets": 25,
        "max_assigned_certificates": 10,
        "deprecation": {
            "announced": "2023-06-01T00:00:00Z",
            "unavailable_after": "2023-09-01T00:00:00Z",
        },
        "prices": [
            {
                "location": "fsn1",
                "price_hourly": {"net": "0.0120", "gross": "0.0120"},
                "price_monthly": {"net": "7.4900", "gross": "7.4900"},
                "price_per_tb_traffic": {"net": "1.0000", "gross": "1.0000"},
                "included_traffic": 21990232555520,
            },
        ],
    }


@pytest.fixture()
def load_balancer_type2():
    return {
        "id": 2,
        "name": "lb21",
        "description": "LB21",
        "max_connections": 20000,
        "max_services": 15,
        "max_targets": 75,
        "max_assigned_certificates": 25,
        "deprecation": None,
        "prices": [
            {
                "location": "fsn1",
                "price_hourly": {"net": "0.0344", "gross": "0.0344"},
                "price_monthly": {"net": "21.4900", "gross": "21.4900"},
                "price_per_tb_traffic": {"net": "1.0000", "gross": "1.0000"},
                "included_traffic": 21990232555520,
            },
        ],
    }
