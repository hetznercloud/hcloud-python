from __future__ import annotations

import datetime
from datetime import timezone

from hcloud.ssh_keys import SSHKey


class TestSSHKey:
    def test_created_is_datetime(self):
        sshKey = SSHKey(id=1, created="2016-01-30T23:50+00:00")
        assert sshKey.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
