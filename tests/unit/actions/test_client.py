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

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["active"],
             "sort": ["status"],
             "page": 2,
             "per_page": 10}
        ]
    )
    def test_get_list(self, actions_client, generic_action_list, params):
        actions_client._client.request.return_value = generic_action_list
        result = actions_client.get_list(**params)
        actions_client._client.request.assert_called_with(url="/actions", method="GET", params=params)

        assert result.meta is None

        actions = result.actions
        assert len(actions) == 2

        action1 = actions[0]
        action2 = actions[1]

        assert action1._client is actions_client
        assert action1.id == 1
        assert action1.command == "start_server"

        assert action2._client is actions_client
        assert action2.id == 2
        assert action2.command == "stop_server"

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["active"],
             "sort": ["status"]}
        ]
    )
    def test_get_all(self, actions_client, generic_action_list, params):
        actions_client._client.request.return_value = generic_action_list
        actions = actions_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        actions_client._client.request.assert_called_with(url="/actions", method="GET", params=params)

        assert len(actions) == 2

        action1 = actions[0]
        action2 = actions[1]

        assert action1._client is actions_client
        assert action1.id == 1
        assert action1.command == "start_server"

        assert action2._client is actions_client
        assert action2.id == 2
        assert action2.command == "stop_server"
