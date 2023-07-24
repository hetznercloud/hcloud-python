from __future__ import annotations

import datetime
from datetime import timezone

from hcloud.servers import Server


class TestServer:
    def test_created_is_datetime(self):
        server = Server(id=1, created="2016-01-30T23:50+00:00")
        assert server.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
