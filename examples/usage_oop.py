from __future__ import annotations

from os import environ

from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

assert (
    "HCLOUD_TOKEN" in environ
), "Please export your API token in the HCLOUD_TOKEN environment variable"
token = environ["HCLOUD_TOKEN"]

# Create a client
client = Client(token=token)

# Create 2 servers
# Create 2 servers
response1 = client.servers.create(
    "Server1", server_type=ServerType(name="cx22"), image=Image(id=4711)
)

response2 = client.servers.create(
    "Server2", server_type=ServerType(name="cx22"), image=Image(id=4711)
)
# Get all servers
server1 = response1.server
server2 = response2.server

servers = client.servers.get_all()

assert servers[0].id == server1.id
assert servers[1].id == server2.id
# Create 2 volumes

response1 = client.volumes.create(size=15, name="Volume1", location=server1.location)
response2 = client.volumes.create(size=10, name="Volume2", location=server2.location)

volume1 = response1.volume
volume2 = response2.volume

# Attach volume to server

volume1.attach(server1)
volume2.attach(server2)

# Detach second volume

volume2.detach()

# Poweroff 2nd server
server2.power_off()
