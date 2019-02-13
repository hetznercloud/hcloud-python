import os
import pytest

from hcloud import HcloudClient


@pytest.fixture(autouse=True, scope='function')
def hetzner_client():
    hetzner_client = HcloudClient(token="test-token", api_endpoint=os.getenv("FAKE_API_ENDPOINT", default="http://localhost:4000"))
    return hetzner_client
