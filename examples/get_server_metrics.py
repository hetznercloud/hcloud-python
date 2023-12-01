from __future__ import annotations

import json
from os import environ

from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

assert (
    "HCLOUD_TOKEN" in environ
), "Please export your API token in the HCLOUD_TOKEN environment variable"
token = environ["HCLOUD_TOKEN"]

client = Client(token=token)

server = client.servers.get_by_name("my-server")
if server is None:
    response = client.servers.create(
        name="my-server",
        server_type=ServerType("cx11"),
        image=Image(name="ubuntu-22.04"),
    )
    server = response.server

response = server.get_metrics(
    type=["cpu", "network"],
    start="2023-12-01T12:00:00+01:00",
    end="2023-12-01T14:00:00+01:00",
)

print(json.dumps(response.metrics))
