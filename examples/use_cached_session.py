from __future__ import annotations

from os import environ

from hcloud import Client

assert (
    "HCLOUD_TOKEN" in environ
), "Please export your API token in the HCLOUD_TOKEN environment variable"
token = environ["HCLOUD_TOKEN"]

client = Client(token=token)

with client.cached_session() as session:
    # This will query the API only once
    for i in range(100):
        servers = session.locations.get_all()

print(servers)
