import mock
import pytest

from hcloud.ssh_keys.client import BoundSSHKey
from hcloud.ssh_keys.domain import SSHKey


class TestBoundSSHKey(object):
    @pytest.fixture()
    def bound_ssh_key(self, hetzner_client):
        return BoundSSHKey(client=hetzner_client.ssh_keys, data=dict(id=42))

    def test_update(self, bound_ssh_key):
        ssh_key = bound_ssh_key.update(name="New name")

        assert ssh_key.id == 2323
        assert ssh_key.name == "New name"

    def test_delete(self, bound_ssh_key):
        delete_success = bound_ssh_key.delete()

        assert delete_success is True


class TestSSHKeysClient(object):
    def test_get_by_id(self, hetzner_client):
        ssh_key = hetzner_client.ssh_keys.get_by_id(1)
        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"
        assert ssh_key.fingerprint == "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        assert ssh_key.public_key == "ssh-rsa AAAjjk76kgf...Xt"

    def test_get_by_name(self, hetzner_client):
        ssh_key = hetzner_client.ssh_keys.get_by_name("My ssh key")
        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"
        assert ssh_key.fingerprint == "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        assert ssh_key.public_key == "ssh-rsa AAAjjk76kgf...Xt"

    def test_get_list(self, hetzner_client):
        ssh_keys = hetzner_client.ssh_keys.get_all()
        assert ssh_keys[0].id == 2323
        assert ssh_keys[0].name == "My ssh key"
        assert ssh_keys[0].fingerprint == "b7:2f:30:a0:2f:6c:58:6c:21:04:58:61:ba:06:3b:2f"
        assert ssh_keys[0].public_key == "ssh-rsa AAAjjk76kgf...Xt"

    def test_create(self, hetzner_client):
        ssh_key = hetzner_client.ssh_keys.create(name="My ssh key", public_key="ssh-rsa AAAjjk76kgf...Xt")

        assert ssh_key.id == 2323
        assert ssh_key.name == "My ssh key"

    @pytest.mark.parametrize("ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, ssh_key):
        ssh_key = hetzner_client.ssh_keys.update(ssh_key, name="New name")

        assert ssh_key.id == 2323
        assert ssh_key.name == "New name"

    @pytest.mark.parametrize("ssh_key", [SSHKey(id=1), BoundSSHKey(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, ssh_key):
        delete_success = hetzner_client.ssh_keys.delete(ssh_key)

        assert delete_success is True
