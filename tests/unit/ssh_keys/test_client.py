from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.ssh_keys import BoundSSHKey, SSHKey, SSHKeysClient

from ..conftest import BoundModelTestCase


class TestBoundSSHKey(BoundModelTestCase):
    methods = [
        BoundSSHKey.update,
        BoundSSHKey.delete,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client) -> SSHKeysClient:
        return client.ssh_keys

    @pytest.fixture()
    def bound_model(self, resource_client: SSHKeysClient) -> BoundSSHKey:
        return BoundSSHKey(resource_client, data=dict(id=14))

    def test_init(self, ssh_key_response):
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


class TestSSHKeysClient:
    @pytest.fixture()
    def ssh_keys_client(self, client: Client):
        return SSHKeysClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        ssh_key_response,
    ):
        request_mock.return_value = ssh_key_response

        ssh_key = ssh_keys_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/ssh_keys/1",
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
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        two_ssh_keys_response,
        params,
    ):
        request_mock.return_value = two_ssh_keys_response

        result = ssh_keys_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/ssh_keys",
            params=params,
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
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        two_ssh_keys_response,
        params,
    ):
        request_mock.return_value = two_ssh_keys_response

        ssh_keys = ssh_keys_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/ssh_keys",
            params=params,
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

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        one_ssh_keys_response,
    ):
        request_mock.return_value = one_ssh_keys_response

        ssh_keys = ssh_keys_client.get_by_name("SSH-Key")

        params = {"name": "SSH-Key"}

        request_mock.assert_called_with(
            method="GET",
            url="/ssh_keys",
            params=params,
        )

        assert ssh_keys._client is ssh_keys_client
        assert ssh_keys.id == 2323
        assert ssh_keys.name == "SSH-Key"

    def test_get_by_fingerprint(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        one_ssh_keys_response,
    ):
        request_mock.return_value = one_ssh_keys_response

        ssh_keys = ssh_keys_client.get_by_fingerprint(
            "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        )

        params = {"fingerprint": "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"}

        request_mock.assert_called_with(
            method="GET",
            url="/ssh_keys",
            params=params,
        )

        assert ssh_keys._client is ssh_keys_client
        assert ssh_keys.id == 2323
        assert ssh_keys.name == "SSH-Key"

    def test_create(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        ssh_key_response,
    ):
        request_mock.return_value = ssh_key_response

        ssh_key = ssh_keys_client.create(
            name="My ssh key", public_key="ssh-rsa AAAjjk76kgf...Xt"
        )

        request_mock.assert_called_with(
            method="POST",
            url="/ssh_keys",
            json={"name": "My ssh key", "public_key": "ssh-rsa AAAjjk76kgf...Xt"},
        )

        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"

    @pytest.mark.parametrize(
        "ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        ssh_key,
        response_update_ssh_key,
    ):
        request_mock.return_value = response_update_ssh_key

        ssh_key = ssh_keys_client.update(ssh_key, name="New name")

        request_mock.assert_called_with(
            method="PUT",
            url="/ssh_keys/1",
            json={"name": "New name"},
        )

        assert ssh_key.id == 2323
        assert ssh_key.name == "New name"

    @pytest.mark.parametrize(
        "ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        ssh_keys_client: SSHKeysClient,
        ssh_key,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = ssh_keys_client.delete(ssh_key)

        request_mock.assert_called_with(
            method="DELETE",
            url="/ssh_keys/1",
        )

        assert delete_success is True
