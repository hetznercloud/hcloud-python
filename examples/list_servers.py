from hcloud import HcloudClient

client = HcloudClient(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
servers = client.servers.get_all()
print(servers)
