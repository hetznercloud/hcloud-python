from hcloud import HcloudClient
from hcloud.images.domain import Image

client = HcloudClient(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
response = client.servers.create(name="my-server", server_type="cx11", image=Image(name="ubuntu-18.04"))
server = response.server
print(server)
print("Root Passwort" + response.root_password)
