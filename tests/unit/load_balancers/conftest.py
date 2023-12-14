from __future__ import annotations

import pytest


@pytest.fixture()
def response_load_balancer():
    return {
        "load_balancer": {
            "id": 4711,
            "name": "Web Frontend",
            "ipv4": "131.232.99.1",
            "ipv6": "2001:db8::1",
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
                "network_zone": "eu-central",
            },
            "load_balancer_type": {
                "id": 1,
                "name": "lb11",
                "description": "lb11",
                "max_connections": 20000,
                "max_services": 5,
                "max_targets": 25,
                "max_assigned_certificates": 10,
                "deprecated": "2016-01-30T23:50:00+00:00",
                "prices": [
                    {
                        "location": "fsn-1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            },
            "protection": {"delete": False},
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "services": [
                {
                    "protocol": "https",
                    "listen_port": 443,
                    "destination_port": 80,
                    "proxyprotocol": False,
                    "http": {
                        "cookie_name": "HCLBSTICKY",
                        "cookie_lifetime": 300,
                        "certificates": [897],
                        "redirect_http": True,
                        "sticky_sessions": True,
                    },
                    "health_check": {
                        "protocol": "http",
                        "port": 4711,
                        "interval": 15,
                        "timeout": 10,
                        "retries": 3,
                        "http": {
                            "domain": "example.com",
                            "path": "/",
                            "response": '{"status": "ok"}',
                            "status_codes": [200],
                            "tls": False,
                        },
                    },
                }
            ],
            "targets": [
                {
                    "type": "server",
                    "server": {"id": 80},
                    "health_status": [{"listen_port": 443, "status": "healthy"}],
                    "label_selector": None,
                    "use_private_ip": False,
                }
            ],
            "algorithm": {"type": "round_robin"},
        }
    }


@pytest.fixture()
def response_create_load_balancer():
    return {
        "load_balancer": {
            "id": 1,
            "name": "my-balancer",
            "load_balancer_type": {
                "id": 1,
                "name": "lb11",
                "description": "lb11",
                "max_connections": 20000,
                "max_services": 5,
                "max_targets": 25,
                "max_assigned_certificates": 10,
                "deprecated": "2016-01-30T23:50:00+00:00",
                "prices": [
                    {
                        "location": "fsn-1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            },
            "network_zone": "eu-central",
            "algorithm": {"type": "round_robin"},
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "services": [
                {
                    "protocol": "https",
                    "listen_port": 443,
                    "destination_port": 80,
                    "proxyprotocol": False,
                    "http": {
                        "cookie_name": "HCLBSTICKY",
                        "cookie_lifetime": 300,
                        "certificates": [897],
                        "redirect_http": True,
                        "sticky_sessions": True,
                    },
                    "health_check": {
                        "protocol": "http",
                        "port": 4711,
                        "interval": 15,
                        "timeout": 10,
                        "retries": 3,
                        "http": {
                            "domain": "example.com",
                            "path": "/",
                            "response": '{"status": "ok"}',
                            "status_codes": [200],
                            "tls": False,
                        },
                    },
                }
            ],
            "targets": [
                {
                    "type": "server",
                    "server": {"id": 80},
                    "label_selector": None,
                    "use_private_ip": False,
                }
            ],
        },
        "action": {
            "id": 1,
            "command": "create_load_balancer",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
    }


@pytest.fixture()
def response_update_load_balancer():
    return {
        "load_balancer": {
            "id": 4711,
            "name": "new-name",
            "ipv4": "131.232.99.1",
            "ipv6": "2001:db8::1",
            "location": {
                "id": 1,
                "name": "fsn1",
                "description": "Falkenstein DC Park 1",
                "country": "DE",
                "city": "Falkenstein",
                "latitude": 50.47612,
                "longitude": 12.370071,
                "network_zone": "eu-central",
            },
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "load_balancer_type": {
                "id": 1,
                "name": "lb11",
                "description": "lb11",
                "max_connections": 20000,
                "max_services": 5,
                "max_targets": 25,
                "max_assigned_certificates": 10,
                "deprecated": "2016-01-30T23:50:00+00:00",
                "prices": [
                    {
                        "location": "fsn-1",
                        "price_hourly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                        "price_monthly": {
                            "net": "1.0000000000",
                            "gross": "1.1900000000000000",
                        },
                    }
                ],
            },
            "protection": {"delete": False},
            "labels": {"labelkey": "value"},
            "created": "2016-01-30T23:50:00+00:00",
            "services": [
                {
                    "protocol": "https",
                    "listen_port": 443,
                    "destination_port": 80,
                    "proxyprotocol": False,
                    "http": {
                        "cookie_name": "HCLBSTICKY",
                        "cookie_lifetime": 300,
                        "certificates": [897],
                        "redirect_http": True,
                        "sticky_sessions": True,
                    },
                    "health_check": {
                        "protocol": "http",
                        "port": 4711,
                        "interval": 15,
                        "timeout": 10,
                        "retries": 3,
                        "http": {
                            "domain": "example.com",
                            "path": "/",
                            "response": '{"status": "ok"}',
                            "status_codes": [200],
                            "tls": False,
                        },
                    },
                }
            ],
            "targets": [
                {
                    "type": "server",
                    "server": {"id": 80},
                    "use_private_ip": False,
                    "health_status": [{"listen_port": 443, "status": "healthy"}],
                    "label_selector": None,
                }
            ],
            "algorithm": {"type": "round_robin"},
        }
    }


@pytest.fixture()
def response_simple_load_balancers():
    return {
        "load_balancers": [
            {
                "id": 4711,
                "name": "Web Frontend",
                "ipv4": "131.232.99.1",
                "ipv6": "2001:db8::1",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                    "network_zone": "eu-central",
                },
                "outgoing_traffic": 123456,
                "ingoing_traffic": 123456,
                "included_traffic": 654321,
                "load_balancer_type": {
                    "id": 1,
                    "name": "lb11",
                    "description": "lb11",
                    "max_connections": 20000,
                    "max_services": 5,
                    "max_targets": 25,
                    "max_assigned_certificates": 10,
                    "deprecated": "2016-01-30T23:50:00+00:00",
                    "prices": [
                        {
                            "location": "fsn-1",
                            "price_hourly": {
                                "net": "1.0000000000",
                                "gross": "1.1900000000000000",
                            },
                            "price_monthly": {
                                "net": "1.0000000000",
                                "gross": "1.1900000000000000",
                            },
                        }
                    ],
                },
                "protection": {"delete": False},
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
                "services": [
                    {
                        "protocol": "https",
                        "listen_port": 443,
                        "destination_port": 80,
                        "proxyprotocol": False,
                        "http": {
                            "sticky_sessions": True,
                            "cookie_name": "HCLBSTICKY",
                            "cookie_lifetime": 300,
                            "certificates": [897],
                            "redirect_http": True,
                        },
                        "health_check": {
                            "protocol": "http",
                            "port": 4711,
                            "interval": 15,
                            "timeout": 10,
                            "retries": 3,
                            "http": {
                                "domain": "example.com",
                                "path": "/",
                                "response": '{"status": "ok"}',
                                "status_codes": [200],
                                "tls": False,
                            },
                        },
                    }
                ],
                "targets": [
                    {
                        "type": "server",
                        "server": {"id": 80},
                        "use_private_ip": False,
                        "health_status": [{"listen_port": 443, "status": "healthy"}],
                        "label_selector": None,
                    }
                ],
                "algorithm": {"type": "round_robin"},
            },
            {
                "id": 4712,
                "name": "Web Frontend2",
                "ipv4": "131.232.99.1",
                "ipv6": "2001:db8::1",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                    "network_zone": "eu-central",
                },
                "load_balancer_type": {
                    "id": 1,
                    "name": "lb11",
                    "description": "lb11",
                    "max_connections": 20000,
                    "max_services": 5,
                    "max_targets": 25,
                    "max_assigned_certificates": 10,
                    "deprecated": "2016-01-30T23:50:00+00:00",
                    "prices": [
                        {
                            "location": "fsn-1",
                            "price_hourly": {
                                "net": "1.0000000000",
                                "gross": "1.1900000000000000",
                            },
                            "price_monthly": {
                                "net": "1.0000000000",
                                "gross": "1.1900000000000000",
                            },
                        }
                    ],
                },
                "protection": {"delete": False},
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
                "outgoing_traffic": 123456,
                "ingoing_traffic": 123456,
                "included_traffic": 654321,
                "services": [
                    {
                        "protocol": "https",
                        "listen_port": 443,
                        "destination_port": 80,
                        "proxyprotocol": False,
                        "http": {
                            "sticky_sessions": True,
                            "cookie_name": "HCLBSTICKY",
                            "cookie_lifetime": 300,
                            "certificates": [897],
                            "redirect_http": True,
                        },
                        "health_check": {
                            "protocol": "http",
                            "port": 4711,
                            "interval": 15,
                            "timeout": 10,
                            "retries": 3,
                            "http": {
                                "domain": "example.com",
                                "path": "/",
                                "response": '{"status": "ok"}',
                                "status_codes": [200],
                                "tls": False,
                            },
                        },
                    }
                ],
                "targets": [
                    {
                        "type": "server",
                        "server": {"id": 80},
                        "health_status": [{"listen_port": 443, "status": "healthy"}],
                        "label_selector": None,
                        "use_private_ip": False,
                    }
                ],
                "algorithm": {"type": "round_robin"},
            },
        ]
    }


@pytest.fixture()
def response_get_metrics():
    return {
        "metrics": {
            "start": "2023-12-14T16:55:32+01:00",
            "end": "2023-12-14T17:25:32+01:00",
            "step": 9.0,
            "time_series": {
                "requests_per_second": {
                    "values": [
                        [1702571114, "0.000000"],
                        [1702571123, "0.000000"],
                        [1702571132, "0.000000"],
                    ]
                }
            },
        }
    }


@pytest.fixture()
def response_add_service():
    return {
        "action": {
            "id": 13,
            "command": "add_service",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_delete_service():
    return {
        "action": {
            "id": 13,
            "command": "delete_service",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_add_target():
    return {
        "action": {
            "id": 13,
            "command": "add_target",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_remove_target():
    return {
        "action": {
            "id": 13,
            "command": "remove_target",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_update_service():
    return {
        "action": {
            "id": 13,
            "command": "update_service",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_change_algorithm():
    return {
        "action": {
            "id": 13,
            "command": "change_algorithm",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_change_reverse_dns_entry():
    return {
        "action": {
            "id": 13,
            "command": "change_dns_ptr",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 42, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_change_protection():
    return {
        "action": {
            "id": 13,
            "command": "change_protection",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_enable_public_interface():
    return {
        "action": {
            "id": 13,
            "command": "enable_public_interface",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_disable_public_interface():
    return {
        "action": {
            "id": 13,
            "command": "disable_public_interface",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_attach_load_balancer_to_network():
    return {
        "action": {
            "id": 13,
            "command": "attach_to_network",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_detach_from_network():
    return {
        "action": {
            "id": 13,
            "command": "detach_from_network",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 4711, "type": "load_balancer"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "change_protection",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 14, "type": "load_balancer"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }
