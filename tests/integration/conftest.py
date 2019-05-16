import os
import pytest

from hcloud import Client


@pytest.fixture(autouse=True, scope='function')
def hetzner_client():
    hetzner_client = Client(token="test-token", api_endpoint=os.getenv("FAKE_API_ENDPOINT", default="http://localhost:4000/v1"))
    return hetzner_client
