import pytest


def test_deprecated_hcloud_hcloud_module():
    with pytest.deprecated_call():
        from hcloud.hcloud import Client  # noqa


def test_deprecated_hcloud_version_constant():
    with pytest.deprecated_call():
        from hcloud.__version__ import VERSION  # noqa
