from __future__ import annotations

from os import environ

from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

assert (
    "HCLOUD_TOKEN" in environ
), "Please export your API token in the HCLOUD_TOKEN environment variable"
token = environ["HCLOUD_TOKEN"]

client = Client(token=token)

response = client.servers.create(
    name="my-server",
    server_type=ServerType(name="cx11"),
    image=Image(name="ubuntu-20.04"),
)
server = response.server
print(server)
print("Root Password" + response.root_password)
