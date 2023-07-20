from __future__ import annotations

import pytest


@pytest.fixture()
def ssh_key_response():
    return {
        "ssh_key": {
            "id": 2323,
            "name": "My ssh key",
            "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
            "public_key": "ssh-rsa AAAjjk76kgf...Xt",
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
        }
    }


@pytest.fixture()
def two_ssh_keys_response():
    return {
        "ssh_keys": [
            {
                "id": 2323,
                "name": "SSH-Key",
                "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
                "public_key": "ssh-rsa AAAjjk76kgf...Xt",
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
            },
            {
                "id": 2324,
                "name": "SSH-Key",
                "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
                "public_key": "ssh-rsa AAAjjk76kgf...Xt",
                "labels": {},
                "created": "2016-01-30T23:50:00+00:00",
            },
        ]
    }


@pytest.fixture()
def one_ssh_keys_response():
    return {
        "ssh_keys": [
            {
                "id": 2323,
                "name": "SSH-Key",
                "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
                "public_key": "ssh-rsa AAAjjk76kgf...Xt",
                "labels": {},
            }
        ]
    }


@pytest.fixture()
def response_update_ssh_key():
    return {
        "ssh_key": {
            "id": 2323,
            "name": "New name",
            "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
            "public_key": "ssh-rsa AAAjjk76kgf...Xt",
            "labels": {},
            "created": "2016-01-30T23:50:00+00:00",
        }
    }
