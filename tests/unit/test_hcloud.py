import pytest


def test_deprecated_hcloud_hcloud_module():
    with pytest.deprecated_call():
        from hcloud.hcloud import Client  # noqa
