response_simple_server = {
    "server": {
        "id": 1,
        "name": "my-server",
        "status": "running",
        "created": "2016-01-30T23:50+00:00",
        "public_net": {},
        "server_type": {},
        "datacenter": {},
        "image": {},
        "iso": {
            "id": 4711,
        },
        "rescue_enabled": False,
        "locked": False,
        "backup_window": "22-02",
        "outgoing_traffic": 123456,
        "ingoing_traffic": 123456,
        "included_traffic": 654321,
        "protection": {},
        "labels": {},
        "volumes": []
    }
}

response_create_simple_server = {
    "server": {
        "id": 1,
        "name": "my-server",
        "status": "running",
        "created": "2016-01-30T23:50+00:00",
        "public_net": {},
        "server_type": {},
        "datacenter": {},
        "image": {},
        "iso": {
            "id": 4711,
        },
        "rescue_enabled": False,
        "locked": False,
        "backup_window": "22-02",
        "outgoing_traffic": 123456,
        "ingoing_traffic": 123456,
        "included_traffic": 654321,
        "protection": {},
        "labels": {},
        "volumes": []
    },
    "action": {
        "id": 1,
        "command": "create_server",
        "status": "running",
        "progress": 0,
        "started": "2016-01-30T23:50+00:00",
        "finished": None,
        "resources": [
            {
                "id": 42,
                "type": "server"
            }
        ],
        "error": {
            "code": "action_failed",
            "message": "Action failed"
        }
    },
    "next_actions": [
        {
            "id": 13,
            "command": "start_server",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [
                {
                    "id": 42,
                    "type": "server"
                }
            ],
            "error": {
                "code": "action_failed",
                "message": "Action failed"
            }
        }
    ],
    "root_password": "YItygq1v3GYjjMomLaKc"
}

response_simple_servers = {
    "servers": [{
        "id": 1,
        "name": "my-server",
        "status": "running",
        "created": "2016-01-30T23:50+00:00",
        "public_net": {},
        "server_type": {},
        "datacenter": {},
        "image": {},
        "iso": {
            "id": 4711,
        },
        "rescue_enabled": False,
        "locked": False,
        "backup_window": "22-02",
        "outgoing_traffic": 123456,
        "ingoing_traffic": 123456,
        "included_traffic": 654321,
        "protection": {},
        "labels": {},
        "volumes": []
    },
        {
            "id": 2,
            "name": "my-server2",
            "status": "running",
            "created": "2016-03-30T23:50+00:00",
            "public_net": {},
            "server_type": {},
            "datacenter": {},
            "image": {},
            "iso": {
                "id": 4712,
            },
            "rescue_enabled": False,
            "locked": False,
            "backup_window": "22-02",
            "outgoing_traffic": 123456,
            "ingoing_traffic": 123456,
            "included_traffic": 654321,
            "protection": {},
            "labels": {},
            "volumes": []
        },
    ]
}

response_full_server = {
    "server": {
        "id": 42,
        "name": "my-server",
        "status": "running",
        "created": "2016-01-30T23:50+00:00",
        "public_net": {
            "ipv4": {
                "ip": "1.2.3.4",
                "blocked": False,
                "dns_ptr": "server01.example.com"
            },
            "ipv6": {
                "ip": "2001:db8::/64",
                "blocked": False,
                "dns_ptr": [
                    {
                        "ip": "2001:db8::1",
                        "dns_ptr": "server.example.com"
                    }
                ]
            },
            "floating_ips": [
                478
            ]
        },
        "server_type": {
            "id": 1,
            "name": "cx11",
            "description": "CX11",
            "cores": 1,
            "memory": 1,
            "disk": 25,
            "prices": [],
            "storage_type": "local",
            "cpu_type": "shared"
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
                "longitude": 12.370071
            },
            "server_types": {
                "supported": [
                    1,
                    2,
                    3
                ],
                "available": [
                    1,
                    2,
                    3
                ]
            }
        },
        "image": {
            "id": 4711,
            "type": "snapshot",
            "status": "available",
            "name": "ubuntu-16.04",
            "description": "Ubuntu 16.04 Standard 64 bit",
            "image_size": 2.3,
            "disk_size": 10,
            "created": "2016-01-30T23:50+00:00",
            "created_from": {
                "id": 1,
                "name": "Server"
            },
            "bound_to": None,
            "os_flavor": "ubuntu",
            "os_version": "16.04",
            "rapid_deploy": False,
            "protection": {
                "delete": False
            },
            "deprecated": "2018-02-28T00:00:00+00:00",
            "labels": {}
        },
        "iso": {
            "id": 4711,
            "name": "FreeBSD-11.0-RELEASE-amd64-dvd1",
            "description": "FreeBSD 11.0 x64",
            "type": "public",
            "deprecated": "2018-02-28T00:00:00+00:00"
        },
        "rescue_enabled": False,
        "locked": False,
        "backup_window": "22-02",
        "outgoing_traffic": 123456,
        "ingoing_traffic": 123456,
        "included_traffic": 654321,
        "protection": {},
        "labels": {},
        "volumes": [1, 2]
    }
}
