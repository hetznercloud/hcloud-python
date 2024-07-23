from __future__ import annotations

from typing import Any, NamedTuple
from unittest import mock

import pytest

from hcloud.actions import ActionsPageResult
from hcloud.core import BaseDomain, BoundModelBase, ClientEntityBase, Meta


class TestBoundModelBase:
    @pytest.fixture()
    def bound_model_class(self):
        class Model(BaseDomain):
            __api_properties__ = ("id", "name", "description")
            __slots__ = __api_properties__

            def __init__(self, id, name="", description=""):
                self.id = id
                self.name = name
                self.description = description

        class BoundModel(BoundModelBase, Model):
            model = Model

        return BoundModel

    @pytest.fixture()
    def client(self):
        client = mock.MagicMock()
        return client

    def test_get_exists_model_attribute_complete_model(self, bound_model_class, client):
        bound_model = bound_model_class(
            client=client,
            data={"id": 1, "name": "name", "description": "my_description"},
        )
        description = bound_model.description
        client.get_by_id.assert_not_called()
        assert description == "my_description"

    def test_get_non_exists_model_attribute_complete_model(
        self, bound_model_class, client
    ):
        bound_model = bound_model_class(
            client=client, data={"id": 1, "name": "name", "description": "description"}
        )
        with pytest.raises(AttributeError):
            bound_model.content
        client.get_by_id.assert_not_called()

    def test_get_exists_model_attribute_incomplete_model(
        self, bound_model_class, client
    ):
        bound_model = bound_model_class(client=client, data={"id": 101}, complete=False)
        client.get_by_id.return_value = bound_model_class(
            client=client,
            data={"id": 101, "name": "name", "description": "super_description"},
        )
        description = bound_model.description
        client.get_by_id.assert_called_once_with(101)
        assert description == "super_description"
        assert bound_model.complete is True

    def test_get_filled_model_attribute_incomplete_model(
        self, bound_model_class, client
    ):
        bound_model = bound_model_class(client=client, data={"id": 101}, complete=False)
        id = bound_model.id
        client.get_by_id.assert_not_called()
        assert id == 101
        assert bound_model.complete is False

    def test_get_non_exists_model_attribute_incomplete_model(
        self, bound_model_class, client
    ):
        bound_model = bound_model_class(client=client, data={"id": 1}, complete=False)
        with pytest.raises(AttributeError):
            bound_model.content
        client.get_by_id.assert_not_called()
        assert bound_model.complete is False


class TestClientEntityBase:
    @pytest.fixture()
    def client_class_constructor(self):
        def constructor(json_content_function):
            class CandiesPageResult(NamedTuple):
                candies: list[Any]
                meta: Meta

            class CandiesClient(ClientEntityBase):
                def get_list(self, status=None, page=None, per_page=None):
                    json_content = json_content_function(page)
                    results = [
                        (r, page, status, per_page) for r in json_content["candies"]
                    ]
                    return CandiesPageResult(results, Meta.parse_meta(json_content))

            return CandiesClient(mock.MagicMock())

        return constructor

    @pytest.fixture()
    def client_class_with_actions_constructor(self):
        def constructor(json_content_function):
            class CandiesClient(ClientEntityBase):
                def get_actions_list(self, status, page=None, per_page=None):
                    json_content = json_content_function(page)
                    results = [
                        (r, page, status, per_page) for r in json_content["actions"]
                    ]
                    return ActionsPageResult(results, Meta.parse_meta(json_content))

            return CandiesClient(mock.MagicMock())

        return constructor

    def test_iter_pages_no_meta(self, client_class_constructor):
        json_content = {"candies": [1, 2]}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client._iter_pages(candies_client.get_list, status="sweet")

        assert result == [(1, 1, "sweet", 50), (2, 1, "sweet", 50)]

    def test_iter_pages_no_next_page(self, client_class_constructor):
        json_content = {
            "candies": [1, 2],
            "meta": {"pagination": {"page": 1, "per_page": 11, "next_page": None}},
        }

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client._iter_pages(candies_client.get_list, status="sweet")

        assert result == [(1, 1, "sweet", 50), (2, 1, "sweet", 50)]

    def test_iter_pages_ok(self, client_class_constructor):
        def json_content_function(p):
            return {
                "candies": [10 + p, 20 + p],
                "meta": {
                    "pagination": {
                        "page": p,
                        "per_page": 11,
                        "next_page": p + 1 if p < 3 else None,
                    }
                },
            }

        candies_client = client_class_constructor(json_content_function)

        result = candies_client._iter_pages(candies_client.get_list, status="sweet")

        assert result == [
            (11, 1, "sweet", 50),
            (21, 1, "sweet", 50),
            (12, 2, "sweet", 50),
            (22, 2, "sweet", 50),
            (13, 3, "sweet", 50),
            (23, 3, "sweet", 50),
        ]

    def test_get_actions_ok(self, client_class_with_actions_constructor):
        def json_content_function(p):
            return {
                "actions": [10 + p, 20 + p],
                "meta": {
                    "pagination": {
                        "page": p,
                        "per_page": 11,
                        "next_page": p + 1 if p < 3 else None,
                    }
                },
            }

        candies_client = client_class_with_actions_constructor(json_content_function)

        result = candies_client._iter_pages(
            candies_client.get_actions_list, status="sweet"
        )

        assert result == [
            (11, 1, "sweet", 50),
            (21, 1, "sweet", 50),
            (12, 2, "sweet", 50),
            (22, 2, "sweet", 50),
            (13, 3, "sweet", 50),
            (23, 3, "sweet", 50),
        ]

    def test_get_first_by_result_exists(self, client_class_constructor):
        json_content = {"candies": [1]}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client._get_first_by(status="sweet")

        assert result == (1, None, "sweet", None)

    def test_get_first_by_result_does_not_exist(self, client_class_constructor):
        json_content = {"candies": []}

        def json_content_function(p):
            return json_content

        candies_client = client_class_constructor(json_content_function)

        result = candies_client._get_first_by(status="sweet")

        assert result is None
