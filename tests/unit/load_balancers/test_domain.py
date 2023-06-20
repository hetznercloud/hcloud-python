import datetime
from datetime import timezone

from hcloud.load_balancers.domain import LoadBalancer


class TestLoadBalancers:
    def test_created_is_datetime(self):
        lb = LoadBalancer(id=1, created="2016-01-30T23:50+00:00")
        assert lb.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=timezone.utc)
