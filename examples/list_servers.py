from __future__ import annotations

from os import environ

from hcloud import Client

assert (
    "HCLOUD_TOKEN" in environ
), "Please export your API token in the HCLOUD_TOKEN environment variable"
token = environ["HCLOUD_TOKEN"]

client = Client(
    token=token,
    application_name="examples",
    application_version="unknown",
)
servers = client.servers.get_all()
print(servers)
