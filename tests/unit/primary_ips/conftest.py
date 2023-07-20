from __future__ import annotations

import pytest


@pytest.fixture()
def primary_ip_response():
    return {
        "primary_ip": {
            "assignee_id": 17,
            "assignee_type": "server",
            "auto_delete": True,
            "blocked": False,
            "created": "2016-01-30T23:55:00+00:00",
            "datacenter": {
                "description": "Falkenstein DC Park 8",
                "id": 42,
                "location": {
                    "city": "Falkenstein",
                    "country": "DE",
                    "description": "Falkenstein DC Park 1",
                    "id": 1,
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                    "name": "fsn1",
                    "network_zone": "eu-central",
                },
                "name": "fsn1-dc8",
                "server_types": {
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                    "supported": [1, 2, 3],
                },
            },
            "dns_ptr": [{"dns_ptr": "server.example.com", "ip": "131.232.99.1"}],
            "id": 42,
            "ip": "131.232.99.1",
            "labels": {},
            "name": "my-resource",
            "protection": {"delete": False},
            "type": "ipv4",
        }
    }


@pytest.fixture()
def one_primary_ips_response():
    return {
        "meta": {
            "pagination": {
                "last_page": 4,
                "next_page": 4,
                "page": 3,
                "per_page": 25,
                "previous_page": 2,
                "total_entries": 100,
            }
        },
        "primary_ips": [
            {
                "assignee_id": 17,
                "assignee_type": "server",
                "auto_delete": True,
                "blocked": False,
                "created": "2016-01-30T23:55:00+00:00",
                "datacenter": {
                    "description": "Falkenstein DC Park 8",
                    "id": 42,
                    "location": {
                        "city": "Falkenstein",
                        "country": "DE",
                        "description": "Falkenstein DC Park 1",
                        "id": 1,
                        "latitude": 50.47612,
                        "longitude": 12.370071,
                        "name": "fsn1",
                        "network_zone": "eu-central",
                    },
                    "name": "fsn1-dc8",
                    "server_types": {
                        "available": [1, 2, 3],
                        "available_for_migration": [1, 2, 3],
                        "supported": [1, 2, 3],
                    },
                },
                "dns_ptr": [{"dns_ptr": "server.example.com", "ip": "131.232.99.1"}],
                "id": 42,
                "ip": "131.232.99.1",
                "labels": {},
                "name": "my-resource",
                "protection": {"delete": False},
                "type": "ipv4",
            }
        ],
    }


@pytest.fixture()
def all_primary_ips_response():
    return {
        "meta": {
            "pagination": {
                "last_page": 1,
                "next_page": None,
                "page": 1,
                "per_page": 25,
                "previous_page": None,
                "total_entries": 1,
            }
        },
        "primary_ips": [
            {
                "assignee_id": 17,
                "assignee_type": "server",
                "auto_delete": True,
                "blocked": False,
                "created": "2016-01-30T23:55:00+00:00",
                "datacenter": {
                    "description": "Falkenstein DC Park 8",
                    "id": 42,
                    "location": {
                        "city": "Falkenstein",
                        "country": "DE",
                        "description": "Falkenstein DC Park 1",
                        "id": 1,
                        "latitude": 50.47612,
                        "longitude": 12.370071,
                        "name": "fsn1",
                        "network_zone": "eu-central",
                    },
                    "name": "fsn1-dc8",
                    "server_types": {
                        "available": [1, 2, 3],
                        "available_for_migration": [1, 2, 3],
                        "supported": [1, 2, 3],
                    },
                },
                "dns_ptr": [{"dns_ptr": "server.example.com", "ip": "131.232.99.1"}],
                "id": 42,
                "ip": "131.232.99.1",
                "labels": {},
                "name": "my-resource",
                "protection": {"delete": False},
                "type": "ipv4",
            }
        ],
    }


@pytest.fixture()
def primary_ip_create_response():
    return {
        "action": {
            "command": "create_primary_ip",
            "error": {"code": "action_failed", "message": "Action failed"},
            "finished": None,
            "id": 13,
            "progress": 0,
            "resources": [{"id": 17, "type": "server"}],
            "started": "2016-01-30T23:50:00+00:00",
            "status": "running",
        },
        "primary_ip": {
            "assignee_id": 17,
            "assignee_type": "server",
            "auto_delete": True,
            "blocked": False,
            "created": "2016-01-30T23:50:00+00:00",
            "datacenter": {
                "description": "Falkenstein DC Park 8",
                "id": 42,
                "location": {
                    "city": "Falkenstein",
                    "country": "DE",
                    "description": "Falkenstein DC Park 1",
                    "id": 1,
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                    "name": "fsn1",
                    "network_zone": "eu-central",
                    "server_types": {
                        "available": [1, 2, 3],
                        "available_for_migration": [1, 2, 3],
                        "supported": [1, 2, 3],
                    },
                },
                "name": "fsn1-dc8",
            },
            "dns_ptr": [{"dns_ptr": "server.example.com", "ip": "2001:db8::1"}],
            "id": 42,
            "ip": "131.232.99.1",
            "labels": {"labelkey": "value"},
            "name": "my-ip",
            "protection": {"delete": False},
            "type": "ipv4",
        },
    }


@pytest.fixture()
def response_update_primary_ip():
    return {
        "primary_ip": {
            "assignee_id": 17,
            "assignee_type": "server",
            "auto_delete": True,
            "blocked": False,
            "created": "2016-01-30T23:55:00+00:00",
            "datacenter": {
                "description": "Falkenstein DC Park 8",
                "id": 42,
                "location": {
                    "city": "Falkenstein",
                    "country": "DE",
                    "description": "Falkenstein DC Park 1",
                    "id": 1,
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                    "name": "fsn1",
                    "network_zone": "eu-central",
                },
                "name": "fsn1-dc8",
                "server_types": {
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                    "supported": [1, 2, 3],
                },
            },
            "dns_ptr": [{"dns_ptr": "server.example.com", "ip": "131.232.99.1"}],
            "id": 42,
            "ip": "131.232.99.1",
            "labels": {},
            "name": "my-resource",
            "protection": {"delete": False},
            "type": "ipv4",
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "assign_primary_ip",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
