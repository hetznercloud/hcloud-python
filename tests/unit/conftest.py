import mock
import pytest


@pytest.fixture(autouse=True, scope='function')
def mocked_requests():
    patcher = mock.patch('hcloud.hcloud.requests')
    mocked_requests = patcher.start()
    yield mocked_requests
    patcher.stop()
