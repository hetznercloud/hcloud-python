from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType

client = Client(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
response = client.servers.create(name="my-server", server_type=ServerType("cx11"), image=Image(name="ubuntu-18.04"))
server = response.server
print(server)
print("Root Password" + response.root_password)
