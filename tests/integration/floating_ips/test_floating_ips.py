import pytest
import mock

from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.floating_ips.client import BoundFloatingIP
from hcloud.floating_ips.domain import FloatingIP


class TestBoundFloatingIPs(object):

    @pytest.fixture()
    def bound_floating_ip(self, hetzner_client):
        return BoundFloatingIP(client=hetzner_client.floating_ips, data=dict(id=4711))

    def test_get_actions(self, bound_floating_ip):
        actions = bound_floating_ip.get_actions()

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"

    def test_update(self, bound_floating_ip):
        floating_ip = bound_floating_ip.update(description="New description", labels={}, name="Web Frontend")
        assert floating_ip.id == 4711
        assert floating_ip.description == "New description"
        assert floating_ip.name == "Web Frontend"

    def test_delete(self, bound_floating_ip):
        delete_success = bound_floating_ip.delete()
        assert delete_success is True

    @pytest.mark.parametrize("server",
                             (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))))
    def test_assign(self, bound_floating_ip, server):
        action = bound_floating_ip.assign(server)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "assign_floating_ip"

    def test_unassign(self, bound_floating_ip):
        action = bound_floating_ip.unassign()
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "unassign_floating_ip"

    def test_change_dns_ptr(self, bound_floating_ip):
        action = bound_floating_ip.change_dns_ptr("1.2.3.4", "server02.example.com")
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "change_dns_ptr"


class TestFloatingIPsClient(object):

    def test_get_by_id(self, hetzner_client):
        bound_floating_ip = hetzner_client.floating_ips.get_by_id(4711)
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"
        assert bound_floating_ip.type == "ipv4"

    def test_get_by_name(self, hetzner_client):
        bound_floating_ip = hetzner_client.floating_ips.get_by_name("Web Frontend")
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.name == "Web Frontend"
        assert bound_floating_ip.description == "Web Frontend"
        assert bound_floating_ip.type == "ipv4"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.floating_ips.get_list()
        bound_floating_ips = result.floating_ips
        assert bound_floating_ips[0].id == 4711
        assert bound_floating_ips[0].description == "Web Frontend"
        assert bound_floating_ips[0].type == "ipv4"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_create(self, hetzner_client, server):
        response = hetzner_client.floating_ips.create(
            type="ipv4",
            description="Web Frontend",
            # home_location=Location(description="fsn1"),
            server=server,
            name="Web Frontend"
        )

        floating_ip = response.floating_ip
        action = response.action

        assert floating_ip.id == 4711
        assert floating_ip.description == "Web Frontend"
        assert floating_ip.type == "ipv4"
        assert floating_ip.name == "Web Frontend"

        assert action.id == 13
        assert action.command == "assign_floating_ip"

    @pytest.mark.parametrize("floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))])
    def test_get_actions(self, hetzner_client, floating_ip):
        actions = hetzner_client.floating_ips.get_actions(floating_ip)

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"

    @pytest.mark.parametrize("floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, floating_ip):
        floating_ip = hetzner_client.floating_ips.update(floating_ip, description="New description", labels={}, name="Web Frontend")

        assert floating_ip.id == 4711
        assert floating_ip.description == "New description"
        assert floating_ip.name == "Web Frontend"

    @pytest.mark.parametrize("floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, floating_ip):
        delete_success = hetzner_client.floating_ips.delete(floating_ip)

        assert delete_success is True

    @pytest.mark.parametrize("server,floating_ip",
                             [(Server(id=43), FloatingIP(id=4711)),
                              (BoundServer(mock.MagicMock(), dict(id=43)), BoundFloatingIP(mock.MagicMock(), dict(id=4711)))])
    def test_assign(self, hetzner_client, server, floating_ip):
        action = hetzner_client.floating_ips.assign(floating_ip, server)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "assign_floating_ip"

    @pytest.mark.parametrize("floating_ip", [FloatingIP(id=4711), BoundFloatingIP(mock.MagicMock(), dict(id=4711))])
    def test_unassign(self, hetzner_client, floating_ip):
        action = hetzner_client.floating_ips.unassign(floating_ip)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "unassign_floating_ip"

    @pytest.mark.parametrize("floating_ip", [FloatingIP(id=4711), BoundFloatingIP(mock.MagicMock(), dict(id=4711))])
    def test_change_dns_ptr(self, hetzner_client, floating_ip):
        action = hetzner_client.floating_ips.change_dns_ptr(floating_ip, "1.2.3.4", "server02.example.com")
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "change_dns_ptr"
