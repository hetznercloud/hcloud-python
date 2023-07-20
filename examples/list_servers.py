from __future__ import annotations

from hcloud import Client

client = Client(
    token="{YOUR_API_TOKEN}"
)  # Please paste your API token here between the quotes
servers = client.servers.get_all()
print(servers)
