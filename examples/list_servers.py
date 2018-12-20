from hcloud import HcloudClient

client = HcloudClient(token="{YOUR_API_TOKEN}")  # Please paste your API token here between the quotes
servers = client.servers.get_all()
print('In this project are {servers_count} Servers\n'.format(servers_count=len(servers)))
for idx, server in enumerate(servers):
    print("Server {index} :\n".format(index=(idx + 1)))
    print('\tServer ID: {server_id}\n'.format(server_id=server.id))
    print('\tServer Name: ' + server.name + '\n')
    print('\tServer IPv4: ' + server.public_net["ipv4"]["ip"] + '\n')
