# Upgrading

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before upgrading, make sure to resolve any deprecation warnings.

## Upgrading to v2

- [#397](https://github.com/hetznercloud/hcloud-python/pull/397): The package version was moved from `hcloud.__version__.VERSION` to `hcloud.__version__`, make sure to update your import paths:

```diff
-from hcloud.__version__ import VERSION
+from hcloud import __version__ as VERSION
```

- [#401](https://github.com/hetznercloud/hcloud-python/pull/401): The deprecated `hcloud.hcloud` module was removed, make sure to update your import paths:

```diff
-from hcloud.hcloud import Client
+from hcloud import Client
```

- [#398](https://github.com/hetznercloud/hcloud-python/pull/398): The [`Client.poll_interval`](#hcloud.Client) property is now private, make sure to configure it while creating the [`Client`](#hcloud.Client):

```diff
-client = Client(token=token)
-client.poll_interval = 2
+client = Client(
+   token=token,
+   poll_interval=2,
+)
```

- [#400](https://github.com/hetznercloud/hcloud-python/pull/400): The [`Client.request`](#hcloud.Client.request) method now returns an empty dict instead of an empty string when the API response is empty:

```diff
 response = client.request(method="DELETE", url="/primary_ips/123456")
-assert response == ""
+assert response == {}
```

- [#402](https://github.com/hetznercloud/hcloud-python/pull/402): In the [`Client.isos.get_list`](#hcloud.isos.client.IsosClient.get_list) and [`Client.isos.get_all`](#hcloud.isos.client.IsosClient.get_all) methods, the deprecated `include_wildcard_architecture` argument was removed, make sure to use the `include_architecture_wildcard` argument instead:

```diff
 client.isos.get_all(
-   include_wildcard_architecture=True,
+   include_architecture_wildcard=True,
 )
```

- [#363](https://github.com/hetznercloud/hcloud-python/pull/363): In the [`Client.primary_ips.create`](#hcloud.primary_ips.client.PrimaryIPsClient.create) method, the `datacenter` argument was moved after `name` argument and is now optional:

```diff
 client.primary_ips.create(
    "ipv4",
-   None,
    "my-ip",
    assignee_id=12345,
 )
```

```diff
 client.primary_ips.create(
    "ipv4",
-   Datacenter(name="fsn1-dc14"),
    "my-ip",
+   datacenter=Datacenter(name="fsn1-dc14"),
 )
```

- [#406](https://github.com/hetznercloud/hcloud-python/pull/406): In the [`Client.servers.rebuild`](#hcloud.servers.client.ServersClient.rebuild) method, the single action return value was deprecated and is now removed. The method now returns a full response wrapping the action and an optional root password:

```diff
-action = client.servers.rebuild(server, image)
+resp = client.servers.rebuild(server, image)
+action = resp.action
+root_password = resp.root_password
```
