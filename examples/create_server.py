from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType

# Please paste your API token here between the quotes
client = Client(token="{YOUR_API_TOKEN}")
response = client.servers.create(
    name="my-server",
    server_type=ServerType("cx11"),
    image=Image(name="ubuntu-20.04"),
)
server = response.server
print(server)
print("Root Password" + response.root_password)
