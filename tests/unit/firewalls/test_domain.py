import datetime
from dateutil.tz import tzoffset

from hcloud.firewalls.domain import Firewall


class TestFirewall(object):
    def test_created_is_datetime(self):
        firewall = Firewall(id=1, created="2016-01-30T23:50+00:00")
        assert firewall.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0)
        )
