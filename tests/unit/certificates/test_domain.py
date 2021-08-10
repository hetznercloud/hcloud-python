import datetime
from dateutil.tz import tzoffset

from hcloud.certificates.domain import Certificate


class TestCertificate(object):
    def test_created_is_datetime(self):
        certificate = Certificate(
            id=1,
            created="2016-01-30T23:50+00:00",
            not_valid_after="2016-01-30T23:50+00:00",
            not_valid_before="2016-01-30T23:50+00:00",
        )
        assert certificate.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0)
        )
        assert certificate.not_valid_after == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0)
        )
        assert certificate.not_valid_before == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0)
        )
