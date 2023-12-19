from __future__ import annotations

import json
from datetime import datetime, timedelta
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

end = datetime.now()
start = end - timedelta(hours=1)

response = server.get_metrics(
    type=["cpu", "network"],
    start=start,
    end=end,
)

print(json.dumps(response.metrics))
