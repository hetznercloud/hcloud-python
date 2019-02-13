import mock
import pytest

from hcloud.actions.client import ActionsClient, BoundAction
from hcloud.actions.domain import Action, ActionFailedException


class TestBoundAction(object):
    @pytest.fixture()
    def bound_running_action(self, mocked_requests):
        return BoundAction(client=ActionsClient(client=mocked_requests), data=dict(id=14, status=Action.STATE_RUNNING))

    def test_wait_until_finished(self, bound_running_action, mocked_requests, running_action, successfully_action):
        mocked_requests.request.side_effect = [running_action, successfully_action]
        bound_running_action.wait_until_finished()
        assert bound_running_action.status == "success"
        assert mocked_requests.request.call_count == 2

    def test_wait_until_finished_with_error(self, bound_running_action, mocked_requests, running_action, failed_action):
        mocked_requests.request.side_effect = [running_action, failed_action]
        with pytest.raises(ActionFailedException) as exception_info:
            bound_running_action.wait_until_finished()

        assert bound_running_action.status == "error"
        assert exception_info.value.action.id == 2


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
