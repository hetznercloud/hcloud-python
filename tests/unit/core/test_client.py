import mock
import pytest

from hcloud.core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result, BaseDomain


class TestBoundModelBase():

    @pytest.fixture()
    def bound_model_class(self):
        class Model(BaseDomain):
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


class TestClientEntityBase():

    @pytest.fixture()
    def client_class_constructor(self):
        def constructor(json_content_function):
            class CandiesClient(ClientEntityBase):
                results_list_attribute_name = 'candies'

                def get_list(self, status, page=None, per_page=None):
                    json_content = json_content_function(page)
                    results = [(r, page, status, per_page) for r in json_content['candies']]
                    return self._add_meta_to_result(results, json_content)
            return CandiesClient(mock.MagicMock())

        return constructor

    @pytest.fixture()
    def client_class_with_actions_constructor(self):
        def constructor(json_content_function):
            class CandiesClient(ClientEntityBase):

                def get_actions_list(self, status, page=None, per_page=None):
                    json_content = json_content_function(page)
                    results = [(r, page, status, per_page) for r in json_content['actions']]
                    return add_meta_to_result(results, json_content, 'actions')
            return CandiesClient(mock.MagicMock())

        return constructor

    def test_get_all_no_meta(self, client_class_constructor):
        json_content = {"candies": [1, 2]}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client.get_all(status="sweet")

        assert result == [(1, 1, "sweet", 50), (2, 1, "sweet", 50)]

    def test_get_all_no_next_page(self, client_class_constructor):
        json_content = {
            "candies": [1, 2],
            "meta": {
                "pagination": {
                    "page": 1,
                    "per_page": 11,
                    "next_page": None
                }
            }
        }

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client.get_all(status="sweet")

        assert result == [(1, 1, "sweet", 50), (2, 1, "sweet", 50)]

    def test_get_all_ok(self, client_class_constructor):
        def json_content_function(p):
            return {
                "candies": [10 + p, 20 + p],
                "meta": {
                    "pagination": {
                        "page": p,
                        "per_page": 11,
                        "next_page": p + 1 if p < 3 else None
                    }
                }
            }

        candies_client = client_class_constructor(json_content_function)

        result = candies_client.get_all(status="sweet")

        assert result == [(11, 1, "sweet", 50), (21, 1, "sweet", 50),
                          (12, 2, "sweet", 50), (22, 2, "sweet", 50),
                          (13, 3, "sweet", 50), (23, 3, "sweet", 50)]

    def test_get_actions_no_method(self, client_class_constructor):
        json_content = {"candies": [1, 2]}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        with pytest.raises(ValueError) as exception_info:
            candies_client.get_actions()
        error = exception_info.value
        assert str(error) == 'this endpoint does not support get_actions method'

    def test_get_actions_ok(self, client_class_with_actions_constructor):
        def json_content_function(p):
            return {
                "actions": [10 + p, 20 + p],
                "meta": {
                    "pagination": {
                        "page": p,
                        "per_page": 11,
                        "next_page": p + 1 if p < 3 else None
                    }
                }
            }

        candies_client = client_class_with_actions_constructor(json_content_function)

        result = candies_client.get_actions(status="sweet")

        assert result == [(11, 1, "sweet", 50), (21, 1, "sweet", 50),
                          (12, 2, "sweet", 50), (22, 2, "sweet", 50),
                          (13, 3, "sweet", 50), (23, 3, "sweet", 50)]

    def test_raise_exception_if_list_attribute_is_not_implemented(self, client_class_with_actions_constructor):
        def json_content_function(p):
            return {
                "actions": [10 + p, 20 + p],
                "meta": {
                    "pagination": {
                        "page": p,
                        "per_page": 11,
                        "next_page": p + 1 if p < 3 else None
                    }
                }
            }

        candies_client = client_class_with_actions_constructor(json_content_function)

        with pytest.raises(NotImplementedError) as exception_info:
            candies_client.get_all()

        error = exception_info.value
        assert str(error) == "in order to get results list, 'results_list_attribute_name' attribute of CandiesClient has to be specified"


class TestGetEntityByNameMixin():
    @pytest.fixture()
    def client_class_constructor(self):
        def constructor(json_content_function):
            class CandiesClient(ClientEntityBase, GetEntityByNameMixin):
                results_list_attribute_name = 'candies'

                def get_list(self, name, page=None, per_page=None):
                    json_content = json_content_function(page)
                    results = json_content['candies']
                    return self._add_meta_to_result(results, json_content)
            return CandiesClient(mock.MagicMock())

        return constructor

    def test_get_by_name_result_exists(self, client_class_constructor):
        json_content = {"candies": [1]}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client.get_by_name(name="sweet")

        assert result == 1

    def test_get_by_name_result_does_not_exist(self, client_class_constructor):
        json_content = {"candies": []}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client.get_by_name(name="sweet")

        assert result is None
