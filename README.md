# Hetzner Cloud Python

[![](https://github.com/hetznercloud/hcloud-python/actions/workflows/test.yml/badge.svg)](https://github.com/hetznercloud/hcloud-python/actions/workflows/test.yml)
[![](https://github.com/hetznercloud/hcloud-python/actions/workflows/lint.yml/badge.svg)](https://github.com/hetznercloud/hcloud-python/actions/workflows/lint.yml)
[![](https://readthedocs.org/projects/hcloud-python/badge/?version=latest)](https://hcloud-python.readthedocs.io)
[![](https://img.shields.io/pypi/pyversions/hcloud.svg)](https://pypi.org/project/hcloud/)

Official Hetzner Cloud python library.

The library's documentation is available at [hcloud-python.readthedocs.io](https://hcloud-python.readthedocs.io), the public API documentation is available at [docs.hetzner.cloud](https://docs.hetzner.cloud).

## Usage

Install the `hcloud` library:

```sh
pip install hcloud
```

For more installation details, please see the [installation docs](https://hcloud-python.readthedocs.io/en/stable/installation.html).

Here is an example that creates a server and list them:

```python
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

client = Client(token="{YOUR_API_TOKEN}")  # Please paste your API token here

# Create a server named my-server
response = client.servers.create(
    name="my-server",
    server_type=ServerType(name="cx11"),
    image=Image(name="ubuntu-22.04"),
)
server = response.server
print(f"{server.id=} {server.name=} {server.status=}")
print(f"root password: {response.root_password}")

# List your servers
servers = client.servers.get_all()
for server in servers:
    print(f"{server.id=} {server.name=} {server.status=}")
```

For more details, please see the [API reference](https://hcloud-python.readthedocs.io/en/stable/api.html).

You can find some more examples under the [`examples/`](https://github.com/hetznercloud/hcloud-python/tree/main/examples) directory.

## Supported Python versions

We support python versions until [`end-of-life`](https://devguide.python.org/versions/#status-of-python-versions).

## Development

First, create a virtual environment and activate it:

```sh
make venv
source venv/bin/activate
```

You may setup [`pre-commit`](https://pre-commit.com/) to run before you commit changes, this removes the need to run it manually afterwards:

```sh
pre-commit install
```

You can then run different tasks defined in the `Makefile`, below are the most important ones:

Build the documentation and open it in your browser:

```sh
make docs
```

Lint the code:

```sh
make lint
```

Run tests using the current `python3` version:

```sh
make test
```

You may also run the tests for multiple `python3` versions using `tox`:

```sh
tox .
```

## License

The MIT License (MIT). Please see [`License File`](https://github.com/hetznercloud/hcloud-python/blob/main/LICENSE) for more information.
