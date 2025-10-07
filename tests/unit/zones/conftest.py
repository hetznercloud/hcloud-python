from __future__ import annotations

import pytest


@pytest.fixture()
def zone1():
    return {
        "id": 42,
        "name": "example1.com",
        "created": "2016-01-30T23:55:00+00:00",
        "mode": "primary",
        "ttl": 10800,
        "protection": {
            "delete": False,
        },
        "labels": {
            "key": "value",
        },
        "primary_nameservers": [
            {"address": "198.51.100.1", "port": 53},
            {"address": "203.0.113.1", "port": 53},
        ],
        "record_count": 0,
        "status": "ok",
        "registrar": "hetzner",
        "authoritative_nameservers": {
            "assigned": [
                "hydrogen.ns.hetzner.com.",
                "oxygen.ns.hetzner.com.",
                "helium.ns.hetzner.de.",
            ],
            "delegated": [
                "hydrogen.ns.hetzner.com.",
                "oxygen.ns.hetzner.com.",
                "helium.ns.hetzner.de.",
            ],
            "delegation_last_check": "2016-01-30T23:55:00+00:00",
            "delegation_status": "valid",
        },
    }


@pytest.fixture()
def zone2():
    return {
        "id": 43,
        "name": "example2.com",
        "created": "2016-01-30T23:55:00+00:00",
        "mode": "secondary",
        "ttl": 10800,
        "protection": {
            "delete": False,
        },
        "labels": {
            "key": "value",
        },
        "primary_nameservers": [
            {"address": "198.51.100.1", "port": 53},
            {"address": "203.0.113.1", "port": 53},
        ],
        "record_count": 0,
        "status": "ok",
        "registrar": "hetzner",
        "authoritative_nameservers": {
            "assigned": [],
            "delegated": [
                "hydrogen.ns.hetzner.com.",
                "oxygen.ns.hetzner.com.",
                "helium.ns.hetzner.de.",
            ],
            "delegation_last_check": "2016-01-30T23:55:00+00:00",
            "delegation_status": "valid",
        },
    }


@pytest.fixture()
def zone_rrset1():
    return {
        "zone": 42,
        "id": "www/A",
        "name": "www",
        "type": "A",
        "ttl": 3600,
        "labels": {"key": "value"},
        "protection": {"change": False},
        "records": [
            {"value": "198.51.100.1", "comment": "web server"},
        ],
    }


@pytest.fixture()
def zone_rrset2():
    return {
        "zone": 42,
        "id": "blog/A",
        "name": "blog",
        "type": "A",
        "ttl": 3600,
        "labels": {"key": "value"},
        "protection": {"change": False},
        "records": [
            {"value": "198.51.100.1", "comment": "web server"},
        ],
    }


@pytest.fixture()
def zone_response(zone1):
    return {"zone": zone1}


@pytest.fixture()
def zone_list_response(zone1, zone2):
    return {
        "zones": [zone1, zone2],
    }


@pytest.fixture()
def zone_create_response(zone1, action1_running):
    return {
        "zone": zone1,
        "action": action1_running,
    }


@pytest.fixture()
def zone_rrset_response(zone_rrset1):
    return {
        "rrset": zone_rrset1,
    }


@pytest.fixture()
def zone_rrset_list_response(zone_rrset1, zone_rrset2):
    return {
        "rrsets": [zone_rrset1, zone_rrset2],
    }


@pytest.fixture()
def zone_rrset_create_response(zone_rrset1, action1_running):
    return {
        "rrset": zone_rrset1,
        "action": action1_running,
    }
