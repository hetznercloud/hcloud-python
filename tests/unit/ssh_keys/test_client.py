from __future__ import annotations

from unittest import mock

import pytest

from hcloud.ssh_keys import BoundSSHKey, SSHKey, SSHKeysClient


class TestBoundSSHKey:
    @pytest.fixture()
    def bound_ssh_key(self, hetzner_client):
        return BoundSSHKey(client=hetzner_client.ssh_keys, data=dict(id=14))

    def test_bound_ssh_key_init(self, ssh_key_response):
        bound_ssh_key = BoundSSHKey(
            client=mock.MagicMock(), data=ssh_key_response["ssh_key"]
        )

        assert bound_ssh_key.id == 2323
        assert bound_ssh_key.name == "My ssh key"
        assert (
            bound_ssh_key.fingerprint
            == "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        )
        assert bound_ssh_key.public_key == "ssh-rsa AAAjjk76kgf...Xt"

    def test_update(self, hetzner_client, bound_ssh_key, response_update_ssh_key):
        hetzner_client.request.return_value = response_update_ssh_key
        ssh_key = bound_ssh_key.update(name="New name")
        hetzner_client.request.assert_called_with(
            url="/ssh_keys/14", method="PUT", json={"name": "New name"}
        )

        assert ssh_key.id == 2323
        assert ssh_key.name == "New name"

    def test_delete(self, hetzner_client, bound_ssh_key, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_ssh_key.delete()
        hetzner_client.request.assert_called_with(url="/ssh_keys/14", method="DELETE")

        assert delete_success is True


class TestSSHKeysClient:
    @pytest.fixture()
    def ssh_keys_client(self):
        return SSHKeysClient(client=mock.MagicMock())

    def test_get_by_id(self, ssh_keys_client, ssh_key_response):
        ssh_keys_client._client.request.return_value = ssh_key_response
        ssh_key = ssh_keys_client.get_by_id(1)
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys/1", method="GET"
        )
        assert ssh_key._client is ssh_keys_client
        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "My ssh key",
                "fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f",
                "label_selector": "k==v",
                "page": 1,
                "per_page": 10,
            },
            {"name": ""},
            {},
        ],
    )
    def test_get_list(self, ssh_keys_client, two_ssh_keys_response, params):
        ssh_keys_client._client.request.return_value = two_ssh_keys_response
        result = ssh_keys_client.get_list(**params)
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys", method="GET", params=params
        )

        ssh_keys = result.ssh_keys
        assert len(ssh_keys) == 2

        ssh_keys1 = ssh_keys[0]
        ssh_keys2 = ssh_keys[1]

        assert ssh_keys1._client is ssh_keys_client
        assert ssh_keys1.id == 2323
        assert ssh_keys1.name == "SSH-Key"

        assert ssh_keys2._client is ssh_keys_client
        assert ssh_keys2.id == 2324
        assert ssh_keys2.name == "SSH-Key"

    @pytest.mark.parametrize(
        "params", [{"name": "My ssh key", "label_selector": "label1"}, {}]
    )
    def test_get_all(self, ssh_keys_client, two_ssh_keys_response, params):
        ssh_keys_client._client.request.return_value = two_ssh_keys_response
        ssh_keys = ssh_keys_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys", method="GET", params=params
        )

        assert len(ssh_keys) == 2

        ssh_keys1 = ssh_keys[0]
        ssh_keys2 = ssh_keys[1]

        assert ssh_keys1._client is ssh_keys_client
        assert ssh_keys1.id == 2323
        assert ssh_keys1.name == "SSH-Key"

        assert ssh_keys2._client is ssh_keys_client
        assert ssh_keys2.id == 2324
        assert ssh_keys2.name == "SSH-Key"

    def test_get_by_name(self, ssh_keys_client, one_ssh_keys_response):
        ssh_keys_client._client.request.return_value = one_ssh_keys_response
        ssh_keys = ssh_keys_client.get_by_name("SSH-Key")

        params = {"name": "SSH-Key"}
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys", method="GET", params=params
        )

        assert ssh_keys._client is ssh_keys_client
        assert ssh_keys.id == 2323
        assert ssh_keys.name == "SSH-Key"

    def test_get_by_fingerprint(self, ssh_keys_client, one_ssh_keys_response):
        ssh_keys_client._client.request.return_value = one_ssh_keys_response
        ssh_keys = ssh_keys_client.get_by_fingerprint(
            "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        )

        params = {"fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"}
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys", method="GET", params=params
        )

        assert ssh_keys._client is ssh_keys_client
        assert ssh_keys.id == 2323
        assert ssh_keys.name == "SSH-Key"

    def test_create(self, ssh_keys_client, ssh_key_response):
        ssh_keys_client._client.request.return_value = ssh_key_response
        ssh_key = ssh_keys_client.create(
            name="My ssh key", public_key="ssh-rsa AAAjjk76kgf...Xt"
        )
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys",
            method="POST",
            json={"name": "My ssh key", "public_key": "ssh-rsa AAAjjk76kgf...Xt"},
        )

        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"

    @pytest.mark.parametrize(
        "ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))]
    )
    def test_update(self, ssh_keys_client, ssh_key, response_update_ssh_key):
        ssh_keys_client._client.request.return_value = response_update_ssh_key
        ssh_key = ssh_keys_client.update(ssh_key, name="New name")
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys/1", method="PUT", json={"name": "New name"}
        )

        assert ssh_key.id == 2323
        assert ssh_key.name == "New name"

    @pytest.mark.parametrize(
        "ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, ssh_keys_client, ssh_key, generic_action):
        ssh_keys_client._client.request.return_value = generic_action
        delete_success = ssh_keys_client.delete(ssh_key)
        ssh_keys_client._client.request.assert_called_with(
            url="/ssh_keys/1", method="DELETE"
        )

        assert delete_success is True
