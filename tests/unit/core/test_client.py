import mock
import pytest

from hcloud.core.client import BoundModelBase


class TestBoundModelBase():

    @pytest.fixture()
    def bound_model_class(self):
        class Model(object):
            __slots__ = ("id", "name", "description")

            def __init__(self, id, name="", description=""):
                self.id = id
                self.name = name
                self.description = description

        class BoundModel(BoundModelBase):
            model = Model

        return BoundModel

    @pytest.fixture()
    def client(self):
        client = mock.MagicMock()
        return client

    def test_get_exists_model_attribute_complete_model(self, bound_model_class, client):
        bound_model = bound_model_class(client=client, data={"id": 1, "name": "name", "description": "my_description"})
        description = bound_model.description
        client.get_by_id.assert_not_called()
        assert description == "my_description"

    def test_get_non_exists_model_attribute_complete_model(self, bound_model_class, client):
        bound_model = bound_model_class(client=client, data={"id": 1, "name": "name", "description": "description"})
        with pytest.raises(AttributeError):
            bound_model.content
        client.get_by_id.assert_not_called()

    def test_get_exists_model_attribute_incomplete_model(self, bound_model_class, client):
        bound_model = bound_model_class(client=client, data={"id": 101}, complete=False)
        client.get_by_id.return_value = bound_model_class(client=client, data={"id": 101, "name": "name", "description": "super_description"})
        description = bound_model.description
        client.get_by_id.assert_called_once_with(101)
        assert description == "super_description"
        assert bound_model.complete is True

    def test_get_filled_model_attribute_incomplete_model(self, bound_model_class, client):
        bound_model = bound_model_class(client=client, data={"id": 101}, complete=False)
        id = bound_model.id
        client.get_by_id.assert_not_called()
        assert id == 101
        assert bound_model.complete is False

    def test_get_non_exists_model_attribute_incomplete_model(self, bound_model_class, client):
        bound_model = bound_model_class(client=client, data={"id": 1}, complete=False)
        with pytest.raises(AttributeError):
            bound_model.content
        client.get_by_id.assert_not_called()
        assert bound_model.complete is False
