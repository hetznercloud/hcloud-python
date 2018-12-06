import mock
import pytest

from hcloud.actions.client import ActionsClient


class TestActionsClient(object):

    @pytest.fixture()
    def actions_client(self):
        return ActionsClient(client=mock.MagicMock())

    def test_get_by_id(self, actions_client, generic_action):
        actions_client._client.request.return_value = generic_action
        action = actions_client.get_by_id(1)
        actions_client._client.request.assert_called_with(url="/actions/1", method="GET")
        assert action._client is actions_client
        assert action.id == 1
        assert action.command == "stop_server"

    def test_get_all_no_params(self, actions_client, generic_action_list):
        actions_client._client.request.return_value = generic_action_list
        actions = actions_client.get_all()
        actions_client._client.request.assert_called_with(url="/actions", method="GET", params={})

        assert len(actions) == 2

        action1 = actions[0]
        action2 = actions[1]

        assert action1._client is actions_client
        assert action1.id == 1
        assert action1.command == "start_server"

        assert action2._client is actions_client
        assert action2.id == 2
        assert action2.command == "stop_server"
