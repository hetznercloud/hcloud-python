from __future__ import annotations

import pytest

from hcloud.load_balancer_types import LoadBalancerType


@pytest.mark.parametrize(
    "value",
    [
        (LoadBalancerType(id=1),),
    ],
)
def test_eq(value):
    assert value == value
