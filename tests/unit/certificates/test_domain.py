from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.certificates import (
    Certificate,
    ManagedCertificateError,
    ManagedCertificateStatus,
)


@pytest.mark.parametrize(
    "value",
    [
        (Certificate(id=1),),
        (ManagedCertificateError()),
        (ManagedCertificateStatus()),
    ],
)
def test_eq(value):
    assert value == value


class TestCertificate:
    def test_created_is_datetime(self):
        certificate = Certificate(
            id=1,
            created="2016-01-30T23:50+00:00",
            not_valid_after="2016-01-30T23:50+00:00",
            not_valid_before="2016-01-30T23:50+00:00",
        )
        assert certificate.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
        assert certificate.not_valid_after == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
        assert certificate.not_valid_before == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
