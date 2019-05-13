import datetime
from dateutil.tz import tzoffset

from hcloud.floating_ips.domain import FloatingIP


class TestFloatingIP(object):

    def test_created_is_datetime(self):
        floatingIP = FloatingIP(id=1, created="2016-01-30T23:50+00:00")
        assert floatingIP.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0))
