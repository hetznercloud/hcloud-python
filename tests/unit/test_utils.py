from __future__ import annotations

import time

from hcloud._utils import batched, waiter


def test_batched():
    assert list(o for o in batched([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]


def test_waiter():
    wait = waiter(timeout=0.2)
    assert wait(0.1) is False
    time.sleep(0.2)
    assert wait(1) is True

    # Clamp sleep to deadline
    wait = waiter(timeout=0.2)
    assert wait(0.3) is False
    assert wait(1) is True
