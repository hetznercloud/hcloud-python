import datetime
from dateutil.tz import tzoffset

from hcloud.isos.domain import Iso


class TestIso(object):
    def test_deprecated_is_datetime(self):
        iso = Iso(id=1, deprecated="2016-01-30T23:50+00:00")
        assert iso.deprecated == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0)
        )
