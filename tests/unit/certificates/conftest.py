from __future__ import annotations

import pytest


@pytest.fixture()
def certificate_response():
    return {
        "certificate": {
            "id": 2323,
            "name": "My Certificate",
            "type": "managed",
            "labels": {},
            "certificate": "-----BEGIN CERTIFICATE-----\n...",
            "created": "2019-01-08T12:10:00+00:00",
            "not_valid_before": "2019-01-08T10:00:00+00:00",
            "not_valid_after": "2019-07-08T09:59:59+00:00",
            "domain_names": ["example.com", "webmail.example.com", "www.example.com"],
            "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
            "status": {
                "issuance": "failed",
                "renewal": "scheduled",
                "error": {"code": "error_code", "message": "error message"},
            },
            "used_by": [{"id": 42, "type": "server"}],
        }
    }


@pytest.fixture()
def create_managed_certificate_response():
    return {
        "certificate": {
            "id": 2323,
            "name": "My Certificate",
            "type": "managed",
            "labels": {},
            "certificate": "-----BEGIN CERTIFICATE-----\n...",
            "created": "2019-01-08T12:10:00+00:00",
            "not_valid_before": "2019-01-08T10:00:00+00:00",
            "not_valid_after": "2019-07-08T09:59:59+00:00",
            "domain_names": ["example.com", "webmail.example.com", "www.example.com"],
            "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
            "status": {"issuance": "pending", "renewal": "scheduled", "error": None},
            "used_by": [{"id": 42, "type": "load_balancer"}],
        },
        "action": {
            "id": 14,
            "command": "issue_certificate",
            "status": "success",
            "progress": 100,
            "started": "2021-01-30T23:55:00+00:00",
            "finished": "2021-01-30T23:57:00+00:00",
            "resources": [{"id": 896, "type": "certificate"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        },
    }


@pytest.fixture()
def two_certificates_response():
    return {
        "certificates": [
            {
                "id": 2323,
                "name": "My Certificate",
                "labels": {},
                "type": "uploaded",
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com",
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
                "status": None,
                "used_by": [{"id": 42, "type": "load_balancer"}],
            },
            {
                "id": 2324,
                "name": "My website cert",
                "labels": {},
                "type": "uploaded",
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com",
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
                "status": None,
                "used_by": [{"id": 42, "type": "load_balancer"}],
            },
        ]
    }


@pytest.fixture()
def one_certificates_response():
    return {
        "certificates": [
            {
                "id": 2323,
                "name": "My Certificate",
                "labels": {},
                "type": "uploaded",
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com",
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
                "status": None,
                "used_by": [{"id": 42, "type": "load_balancer"}],
            }
        ]
    }


@pytest.fixture()
def response_update_certificate():
    return {
        "certificate": {
            "id": 2323,
            "name": "New name",
            "labels": {},
            "type": "uploaded",
            "certificate": "-----BEGIN CERTIFICATE-----\n...",
            "created": "2019-01-08T12:10:00+00:00",
            "not_valid_before": "2019-01-08T10:00:00+00:00",
            "not_valid_after": "2019-07-08T09:59:59+00:00",
            "domain_names": ["example.com", "webmail.example.com", "www.example.com"],
            "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f",
            "status": None,
            "used_by": [{"id": 42, "type": "load_balancer"}],
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
                "resources": [{"id": 14, "type": "certificate"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            }
        ]
    }


@pytest.fixture()
def response_retry_issuance_action():
    return {
        "action": {
            "id": 14,
            "command": "issue_certificate",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "certificate"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }
