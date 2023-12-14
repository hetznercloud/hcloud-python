from __future__ import annotations

import pytest


@pytest.fixture()
def response_simple_server():
    return {
        "server": {
            "id": 1,
            "name": "my-server",
            "status": "running",
            "created": "2016-01-30T23:50+00:00",
            "public_net": {
                "ipv4": {
                    "ip": "1.2.3.4",
                    "id": 1,
                    "blocked": False,
                    "dns_ptr": "server01.example.com",
                },
                "ipv6": {
                    "ip": "2001:db8::/64",
                    "blocked": False,
                    "id": 2,
                    "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                },
                "floating_ips": [478],
                "firewalls": [{"id": 38, "status": "applied"}],
            },
            "private_net": [
                {
                    "network": 4711,
                    "ip": "10.1.1.5",
                    "alias_ips": ["10.1.1.8"],
                    "mac_address": "86:00:ff:2a:7d:e1",
                }
            ],
            "server_type": {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
                "prices": [
                    {
                        "location": "fsn1",
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
                "storage_type": "local",
                "cpu_type": "shared",
            },
            "datacenter": {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
            "image": {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "rapid_deploy": False,
                "protection": {"delete": False, "rebuild": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
            "iso": None,
            "rescue_enabled": False,
            "locked": False,
            "backup_window": "22-02",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "primary_disk_size": 20,
            "protection": {},
            "labels": {},
            "volumes": [],
        }
    }


@pytest.fixture()
def response_create_simple_server():
    return {
        "server": {
            "id": 1,
            "name": "my-server",
            "status": "running",
            "created": "2016-01-30T23:50+00:00",
            "primary_disk_size": 20,
            "public_net": {
                "ipv4": {
                    "ip": "1.2.3.4",
                    "blocked": False,
                    "id": 1,
                    "dns_ptr": "server01.example.com",
                },
                "ipv6": {
                    "ip": "2001:db8::/64",
                    "blocked": False,
                    "id": 2,
                    "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                },
                "floating_ips": [],
                "firewalls": [{"id": 38, "status": "applied"}],
            },
            "private_net": [],
            "server_type": {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
                "prices": [
                    {
                        "location": "fsn1",
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
                "storage_type": "local",
                "cpu_type": "shared",
            },
            "datacenter": {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
            "image": {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "rapid_deploy": False,
                "protection": {"delete": False, "rebuild": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
            "iso": {"id": 4711},
            "rescue_enabled": False,
            "locked": False,
            "backup_window": "22-02",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "protection": {},
            "labels": {},
            "volumes": [],
        },
        "action": {
            "id": 1,
            "command": "create_server",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
        "next_actions": [
            {
                "id": 13,
                "command": "start_server",
                "status": "running",
                "progress": 0,
                "started": "2016-01-30T23:50+00:00",
                "finished": None,
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ],
        "root_password": "YItygq1v3GYjjMomLaKc",
    }


@pytest.fixture()
def response_update_server():
    return {
        "server": {
            "id": 14,
            "name": "new-name",
            "status": "running",
            "created": "2016-01-30T23:50+00:00",
            "public_net": {
                "ipv4": {
                    "ip": "1.2.3.4",
                    "blocked": False,
                    "id": 1,
                    "dns_ptr": "server01.example.com",
                },
                "ipv6": {
                    "ip": "2001:db8::/64",
                    "blocked": False,
                    "id": 2,
                    "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                },
                "floating_ips": [478],
                "firewalls": [],
            },
            "private_net": [],
            "server_type": {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
                "prices": [
                    {
                        "location": "fsn1",
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
                "storage_type": "local",
                "cpu_type": "shared",
            },
            "datacenter": {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
            "image": {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "rapid_deploy": False,
                "protection": {"delete": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
            "iso": {
                "id": 4711,
                "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
                "description": "FreeBSD 11.0 x64",
                "type": "public",
                "deprecated": "2018-02-28T00:00:00+00:00",
            },
            "rescue_enabled": False,
            "locked": False,
            "backup_window": "22-02",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "protection": {"delete": False, "rebuild": False},
            "labels": {},
            "volumes": [],
        }
    }


@pytest.fixture()
def response_get_metrics():
    return {
        "metrics": {
            "start": "2023-12-14T17:40:00+01:00",
            "end": "2023-12-14T17:50:00+01:00",
            "step": 3.0,
            "time_series": {
                "cpu": {
                    "values": [
                        [1702572594, "0.3746000025854892"],
                        [1702572597, "0.35842215349409734"],
                        [1702572600, "0.7381525488039541"],
                    ]
                },
                "disk.0.iops.read": {
                    "values": [
                        [1702572594, "0"],
                        [1702572597, "0"],
                        [1702572600, "0"],
                    ]
                },
                "disk.0.bandwidth.read": {
                    "values": [
                        [1702572594, "0"],
                        [1702572597, "0"],
                        [1702572600, "0"],
                    ]
                },
                "disk.0.bandwidth.write": {
                    "values": [
                        [1702572594, "24064"],
                        [1702572597, "2048"],
                        [1702572600, "0"],
                    ]
                },
                "disk.0.iops.write": {
                    "values": [
                        [1702572594, "4.875"],
                        [1702572597, "0.25"],
                        [1702572600, "0"],
                    ]
                },
            },
        }
    }


@pytest.fixture()
def response_simple_servers():
    return {
        "servers": [
            {
                "id": 1,
                "name": "my-server",
                "status": "running",
                "created": "2016-01-30T23:50+00:00",
                "public_net": {
                    "ipv4": {
                        "ip": "1.2.3.4",
                        "blocked": False,
                        "id": 2,
                        "dns_ptr": "server01.example.com",
                    },
                    "ipv6": {
                        "ip": "2001:db8::/64",
                        "blocked": False,
                        "id": 1,
                        "dns_ptr": [
                            {"ip": "2001:db8::1", "dns_ptr": "server.example.com"}
                        ],
                    },
                    "floating_ips": [478],
                    "firewalls": [],
                },
                "private_net": [
                    {
                        "network": 4711,
                        "ip": "10.1.1.5",
                        "alias_ips": ["10.1.1.8"],
                        "mac_address": "86:00:ff:2a:7d:e1",
                    }
                ],
                "server_type": {
                    "id": 1,
                    "name": "cx11",
                    "description": "CX11",
                    "cores": 1,
                    "memory": 1,
                    "disk": 25,
                    "prices": [
                        {
                            "location": "fsn1",
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
                    "storage_type": "local",
                    "cpu_type": "shared",
                },
                "datacenter": {
                    "id": 1,
                    "name": "fsn1-dc8",
                    "description": "Falkenstein 1 DC 8",
                    "location": {
                        "id": 1,
                        "name": "fsn1",
                        "description": "Falkenstein DC Park 1",
                        "country": "DE",
                        "city": "Falkenstein",
                        "latitude": 50.47612,
                        "longitude": 12.370071,
                    },
                    "server_types": {
                        "supported": [1, 2, 3],
                        "available": [1, 2, 3],
                        "available_for_migration": [1, 2, 3],
                    },
                },
                "image": {
                    "id": 4711,
                    "type": "snapshot",
                    "status": "available",
                    "name": "ubuntu-20.04",
                    "description": "Ubuntu 20.04 Standard 64 bit",
                    "image_size": 2.3,
                    "disk_size": 10,
                    "created": "2016-01-30T23:50+00:00",
                    "created_from": {"id": 1, "name": "Server"},
                    "bound_to": None,
                    "os_flavor": "ubuntu",
                    "os_version": "16.04",
                    "rapid_deploy": False,
                    "protection": {"delete": False, "rebuild": False},
                    "deprecated": "2018-02-28T00:00:00+00:00",
                    "labels": {},
                },
                "iso": None,
                "rescue_enabled": False,
                "locked": False,
                "backup_window": "22-02",
                "outgoing_traffic": 123456,
                "ingoing_traffic": 123456,
                "included_traffic": 654321,
                "protection": {},
                "labels": {},
                "volumes": [],
            },
            {
                "id": 2,
                "name": "my-server2",
                "status": "running",
                "created": "2016-03-30T23:50+00:00",
                "public_net": {
                    "ipv4": {
                        "ip": "1.2.3.4",
                        "blocked": False,
                        "id": 3,
                        "dns_ptr": "server01.example.com",
                    },
                    "ipv6": {
                        "ip": "2001:db8::/64",
                        "blocked": False,
                        "id": 4,
                        "dns_ptr": [
                            {"ip": "2001:db8::1", "dns_ptr": "server.example.com"}
                        ],
                    },
                    "floating_ips": [478],
                    "firewalls": [],
                },
                "private_net": [
                    {
                        "network": 4711,
                        "ip": "10.1.1.7",
                        "alias_ips": ["10.1.1.99"],
                        "mac_address": "86:00:ff:2a:7d:e1",
                    }
                ],
                "server_type": {
                    "id": 1,
                    "name": "cx11",
                    "description": "CX11",
                    "cores": 1,
                    "memory": 1,
                    "disk": 25,
                    "prices": [
                        {
                            "location": "fsn1",
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
                    "storage_type": "local",
                    "cpu_type": "shared",
                },
                "datacenter": {
                    "id": 1,
                    "name": "fsn1-dc8",
                    "description": "Falkenstein 1 DC 8",
                    "location": {
                        "id": 1,
                        "name": "fsn1",
                        "description": "Falkenstein DC Park 1",
                        "country": "DE",
                        "city": "Falkenstein",
                        "latitude": 50.47612,
                        "longitude": 12.370071,
                    },
                    "server_types": {
                        "supported": [1, 2, 3],
                        "available": [1, 2, 3],
                        "available_for_migration": [1, 2, 3],
                    },
                },
                "image": {
                    "id": 4711,
                    "type": "snapshot",
                    "status": "available",
                    "name": "ubuntu-20.04",
                    "description": "Ubuntu 20.04 Standard 64 bit",
                    "image_size": 2.3,
                    "disk_size": 10,
                    "created": "2016-01-30T23:50+00:00",
                    "created_from": {"id": 1, "name": "Server"},
                    "bound_to": None,
                    "os_flavor": "ubuntu",
                    "os_version": "16.04",
                    "rapid_deploy": False,
                    "protection": {"delete": False, "rebuild": False},
                    "deprecated": "2018-02-28T00:00:00+00:00",
                    "labels": {},
                },
                "iso": None,
                "rescue_enabled": False,
                "locked": False,
                "backup_window": "22-02",
                "outgoing_traffic": 123456,
                "ingoing_traffic": 123456,
                "included_traffic": 654321,
                "primary_disk_size": 20,
                "protection": {},
                "labels": {},
                "volumes": [],
            },
        ]
    }


@pytest.fixture()
def response_full_server():
    return {
        "server": {
            "id": 42,
            "name": "my-server",
            "status": "running",
            "created": "2016-01-30T23:50+00:00",
            "primary_disk_size": 20,
            "public_net": {
                "ipv4": {
                    "ip": "1.2.3.4",
                    "blocked": False,
                    "id": 1,
                    "dns_ptr": "server01.example.com",
                },
                "ipv6": {
                    "ip": "2001:db8::/64",
                    "blocked": False,
                    "id": 2,
                    "dns_ptr": [{"ip": "2001:db8::1", "dns_ptr": "server.example.com"}],
                },
                "floating_ips": [478],
                "firewalls": [{"id": 38, "status": "applied"}],
            },
            "private_net": [
                {
                    "network": 4711,
                    "ip": "10.1.1.5",
                    "alias_ips": ["10.1.1.8"],
                    "mac_address": "86:00:ff:2a:7d:e1",
                }
            ],
            "server_type": {
                "id": 1,
                "name": "cx11",
                "description": "CX11",
                "cores": 1,
                "memory": 1,
                "disk": 25,
                "prices": [],
                "storage_type": "local",
                "cpu_type": "shared",
            },
            "datacenter": {
                "id": 1,
                "name": "fsn1-dc8",
                "description": "Falkenstein 1 DC 8",
                "location": {
                    "id": 1,
                    "name": "fsn1",
                    "description": "Falkenstein DC Park 1",
                    "country": "DE",
                    "city": "Falkenstein",
                    "latitude": 50.47612,
                    "longitude": 12.370071,
                },
                "server_types": {
                    "supported": [1, 2, 3],
                    "available": [1, 2, 3],
                    "available_for_migration": [1, 2, 3],
                },
            },
            "image": {
                "id": 4711,
                "type": "snapshot",
                "status": "available",
                "name": "ubuntu-20.04",
                "description": "Ubuntu 20.04 Standard 64 bit",
                "image_size": 2.3,
                "disk_size": 10,
                "created": "2016-01-30T23:50+00:00",
                "created_from": {"id": 1, "name": "Server"},
                "bound_to": None,
                "os_flavor": "ubuntu",
                "os_version": "16.04",
                "rapid_deploy": False,
                "protection": {"delete": False},
                "deprecated": "2018-02-28T00:00:00+00:00",
                "labels": {},
            },
            "iso": {
                "id": 4711,
                "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
                "description": "FreeBSD 11.0 x64",
                "type": "public",
                "deprecated": "2018-02-28T00:00:00+00:00",
            },
            "placement_group": {
                "created": "2019-01-08T12:10:00+00:00",
                "id": 897,
                "labels": {"key": "value"},
                "name": "my Placement Group",
                "servers": [4711, 4712],
                "type": "spread",
            },
            "rescue_enabled": False,
            "locked": False,
            "backup_window": "22-02",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "protection": {},
            "labels": {},
            "volumes": [1, 2],
        }
    }


@pytest.fixture()
def response_server_reset_password():
    return {
        "action": {
            "id": 1,
            "command": "reset_password",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
        "root_password": "YItygq1v3GYjjMomLaKc",
    }


@pytest.fixture()
def response_server_enable_rescue():
    return {
        "action": {
            "id": 1,
            "command": "enable_rescue",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
        "root_password": "YItygq1v3GYjjMomLaKc",
    }


@pytest.fixture()
def response_server_create_image():
    return {
        "image": {
            "id": 4711,
            "type": "snapshot",
            "status": "creating",
            "name": None,
            "description": "my image",
            "image_size": 2.3,
            "disk_size": 10,
            "created": "2016-01-30T23:50+00:00",
            "created_from": {"id": 1, "name": "Server"},
            "bound_to": None,
            "os_flavor": "ubuntu",
            "os_version": "16.04",
            "rapid_deploy": False,
            "protection": {"delete": False},
            "deprecated": "2018-02-28T00:00:00+00:00",
            "labels": {},
        },
        "action": {
            "id": 1,
            "command": "enable_rescue",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
    }


@pytest.fixture()
def response_server_request_console():
    return {
        "wss_url": "wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c",
        "password": "9MQaTg2VAGI0FIpc10k3UpRXcHj2wQ6x",
        "action": {
            "id": 1,
            "command": "request_console",
            "status": "success",
            "progress": 0,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
    }


@pytest.fixture()
def response_get_actions():
    return {
        "actions": [
            {
                "id": 13,
                "command": "start_server",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }


@pytest.fixture()
def response_attach_to_network():
    return {
        "action": {
            "id": 1,
            "command": "attach_to_network",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50:00+00:00",
            "finished": None,
            "resources": [
                {"id": 42, "type": "server"},
                {"id": 4711, "type": "network"},
            ],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_detach_from_network():
    return {
        "action": {
            "id": 1,
            "command": "detach_from_network",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50:00+00:00",
            "finished": None,
            "resources": [
                {"id": 42, "type": "server"},
                {"id": 4711, "type": "network"},
            ],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_change_alias_ips():
    return {
        "action": {
            "id": 1,
            "command": "change_alias_ips",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50:00+00:00",
            "finished": None,
            "resources": [
                {"id": 42, "type": "server"},
                {"id": 4711, "type": "network"},
            ],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_apply_firewall():
    return {
        "action": {
            "id": 1,
            "command": "apply_firewall",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50:00+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_remove_firewall():
    return {
        "action": {
            "id": 1,
            "command": "remove_firewall",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50:00+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def response_add_to_placement_group():
    return {
        "action": {
            "command": "add_to_placement_group",
            "error": {"code": "action_failed", "message": "Action failed"},
            "finished": None,
            "id": 13,
            "progress": 0,
            "resources": [{"id": 42, "type": "server"}],
            "started": "2016-01-30T23:50:00+00:00",
            "status": "running",
        }
    }


@pytest.fixture()
def response_remove_from_placement_group():
    return {
        "action": {
            "command": "remove_from_placement_group",
            "error": {"code": "action_failed", "message": "Action failed"},
            "finished": "2016-01-30T23:56:00+00:00",
            "id": 13,
            "progress": 100,
            "resources": [{"id": 42, "type": "server"}],
            "started": "2016-01-30T23:55:00+00:00",
            "status": "success",
        }
    }
