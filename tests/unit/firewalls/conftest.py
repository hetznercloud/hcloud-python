from __future__ import annotations

import pytest


@pytest.fixture()
def response_create_firewall():
    return {
        "firewall": {
            "id": 38,
            "name": "Corporate Intranet Protection",
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
            "rules": [
                {
                    "direction": "in",
                    "source_ips": [
                        "28.239.13.1/32",
                        "28.239.14.0/24",
                        "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                    ],
                    "destination_ips": [],
                    "protocol": "tcp",
                    "port": "80",
                    "description": None,
                },
                {
                    "direction": "out",
                    "source_ips": [],
                    "destination_ips": [
                        "28.239.13.1/32",
                        "28.239.14.0/24",
                        "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                    ],
                    "protocol": "tcp",
                    "port": "80",
                    "description": "allow http out",
                },
            ],
            "applied_to": [
                {"server": {"id": 42}, "type": "server"},
                {
                    "type": "label_selector",
                    "label_selector": {"selector": "key==value"},
                },
            ],
        },
        "actions": [
            {
                "command": "set_firewall_rules",
                "error": {"code": "action_failed", "message": "Action failed"},
                "finished": "2016-01-30T23:56:00+00:00",
                "id": 13,
                "progress": 100,
                "resources": [{"id": 38, "type": "firewall"}],
                "started": "2016-01-30T23:55:00+00:00",
                "status": "success",
            },
            {
                "command": "apply_firewall",
                "error": {"code": "action_failed", "message": "Action failed"},
                "finished": "2016-01-30T23:56:00+00:00",
                "id": 14,
                "progress": 100,
                "resources": [
                    {"id": 42, "type": "server"},
                    {"id": 38, "type": "firewall"},
                ],
                "started": "2016-01-30T23:55:00+00:00",
                "status": "success",
            },
        ],
    }


@pytest.fixture()
def firewall_response():
    return {
        "firewall": {
            "id": 38,
            "name": "Corporate Intranet Protection",
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
            "rules": [
                {
                    "direction": "in",
                    "source_ips": [
                        "28.239.13.1/32",
                        "28.239.14.0/24",
                        "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                    ],
                    "destination_ips": [],
                    "protocol": "tcp",
                    "port": "80",
                    "description": "allow http in",
                },
                {
                    "direction": "out",
                    "source_ips": [],
                    "destination_ips": [
                        "28.239.13.1/32",
                        "28.239.14.0/24",
                        "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                    ],
                    "protocol": "tcp",
                    "port": "80",
                    "description": "allow http out",
                },
            ],
            "applied_to": [
                {"server": {"id": 42}, "type": "server"},
                {
                    "type": "label_selector",
                    "label_selector": {"selector": "key==value"},
                },
            ],
        }
    }


@pytest.fixture()
def two_firewalls_response():
    return {
        "firewalls": [
            {
                "id": 38,
                "name": "Corporate Intranet Protection",
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
                "rules": [
                    {
                        "direction": "in",
                        "source_ips": [
                            "28.239.13.1/32",
                            "28.239.14.0/24",
                            "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                        ],
                        "destination_ips": [],
                        "protocol": "tcp",
                        "port": "80",
                        "description": "allow http in",
                    }
                ],
                "applied_to": [{"server": {"id": 42}, "type": "server"}],
            },
            {
                "id": 39,
                "name": "Corporate Extranet Protection",
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
                "rules": [
                    {
                        "direction": "in",
                        "destination_ips": [],
                        "source_ips": [
                            "28.239.13.1/32",
                            "28.239.14.0/24",
                            "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                        ],
                        "protocol": "tcp",
                        "port": "443",
                        "description": "allow https in",
                    }
                ],
                "applied_to": [{"server": {"id": 42}, "type": "server"}],
            },
        ]
    }


@pytest.fixture()
def one_firewalls_response():
    return {
        "firewalls": [
            {
                "id": 38,
                "name": "Corporate Intranet Protection",
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
                "rules": [
                    {
                        "direction": "in",
                        "destination_ips": [],
                        "source_ips": [
                            "28.239.13.1/32",
                            "28.239.14.0/24",
                            "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                        ],
                        "protocol": "tcp",
                        "port": "80",
                        "description": "allow http in",
                    }
                ],
                "applied_to": [{"server": {"id": 42}, "type": "server"}],
            }
        ]
    }


@pytest.fixture()
def response_update_firewall():
    return {
        "firewall": {
            "id": 38,
            "name": "New Corporate Intranet Protection",
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
            "rules": [
                {
                    "direction": "in",
                    "source_ips": [
                        "28.239.13.1/32",
                        "28.239.14.0/24",
                        "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
                    ],
                    "destination_ips": [],
                    "protocol": "tcp",
                    "port": "80",
                    "description": "allow http in",
                }
            ],
            "applied_to": [{"server": {"id": 42}, "type": "server"}],
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "set_firewall_rules",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "firewall"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }


@pytest.fixture()
def response_set_rules():
    return {
        "actions": [
            {
                "id": 13,
                "command": "set_firewall_rules",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 38, "type": "firewall"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            },
            {
                "id": 14,
                "command": "apply_firewall",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [
                    {"id": 38, "type": "firewall"},
                    {"id": 42, "type": "server"},
                ],
                "error": {"code": "action_failed", "message": "Action failed"},
            },
        ]
    }
