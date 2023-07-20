from __future__ import annotations

from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.servers.domain import Server
from hcloud.volumes.domain import Volume

client = Client(token="project-token")

# Create 2 servers
response1 = client.servers.create(
    name="Server1", server_type=ServerType(name="cx11"), image=Image(id=4711)
)

response2 = client.servers.create(
    "Server2", server_type=ServerType(name="cx11"), image=Image(id=4711)
)

server1 = response1.server
server2 = response2.server

# Get all servers

servers = client.servers.get_all()

assert servers[0].id == server1.id
assert servers[1].id == server2.id

# Create 2 volumes

response1 = client.volumes.create(size=15, name="Volume1", location=server1.location)
response2 = client.volumes.create(size=10, name="Volume2", location=server2.location)

volume1 = response1.volume
volume2 = response2.volume

# Attach volume to server

client.volumes.attach(server1, volume1)
client.volumes.attach(server2, volume2)

# Detach second volume

client.volumes.detach(volume2)

# Poweroff 2nd server
client.servers.power_off(server2)

# Create one more volume and attach it to server with id=33

server33 = Server(id=33)
response = client.volumes.create(size=33, name="Volume33", server=server33)

print(response.action.status)

# Create one more server and attach 2 volumes to it
client.servers.create(
    "Server3",
    server_type=ServerType(name="cx11"),
    image=Image(id=4711),
    volumes=[Volume(id=221), Volume(id=222)],
)
