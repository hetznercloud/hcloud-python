
class TestActionsClient(object):
    def test_get_by_id(self, hetzner_client):
        action = hetzner_client.actions.get_by_id(13)
        assert action.id == 13
        assert action.command == "start_server"
        assert action.progress == 100

    def test_get_all(self, hetzner_client):
        actions = hetzner_client.actions.get_all()
        assert actions[0].id == 13
        assert actions[0].command == "start_server"
        assert actions[0].progress == 100
