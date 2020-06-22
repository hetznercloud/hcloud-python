import pytest


@pytest.fixture()
def certificate_response():
    return {
        "certificate": {
            "id": 2323,
            "name": "My Certificate",
            "labels": {},
            "certificate": "-----BEGIN CERTIFICATE-----\n...",
            "created": "2019-01-08T12:10:00+00:00",
            "not_valid_before": "2019-01-08T10:00:00+00:00",
            "not_valid_after": "2019-07-08T09:59:59+00:00",
            "domain_names": [
                "example.com",
                "webmail.example.com",
                "www.example.com"
            ],
            "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        }
    }


@pytest.fixture()
def two_certificates_response():
    return {
        "certificates": [
            {
                "id": 2323,
                "name": "My Certificate",
                "labels": {},
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com"
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
            },
            {
                "id": 2324,
                "name": "My website cert",
                "labels": {},
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com"
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
            }
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
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "created": "2019-01-08T12:10:00+00:00",
                "not_valid_before": "2019-01-08T10:00:00+00:00",
                "not_valid_after": "2019-07-08T09:59:59+00:00",
                "domain_names": [
                    "example.com",
                    "webmail.example.com",
                    "www.example.com"
                ],
                "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
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
            "certificate": "-----BEGIN CERTIFICATE-----\n...",
            "created": "2019-01-08T12:10:00+00:00",
            "not_valid_before": "2019-01-08T10:00:00+00:00",
            "not_valid_after": "2019-07-08T09:59:59+00:00",
            "domain_names": [
                "example.com",
                "webmail.example.com",
                "www.example.com"
            ],
            "fingerprint": "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        }
    }
