from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.placement_groups import BoundPlacementGroup, PlacementGroupsClient


def check_variables(placement_group, expected):
    assert placement_group.id == expected["id"]
    assert placement_group.name == expected["name"]
    assert placement_group.labels == expected["labels"]
    assert placement_group.servers == expected["servers"]
    assert placement_group.type == expected["type"]


class TestBoundPlacementGroup:
    @pytest.fixture()
    def bound_placement_group(self, client: Client):
        return BoundPlacementGroup(client.placement_groups, data=dict(id=897))

    def test_bound_placement_group_init(self, placement_group_response):
        bound_placement_group = BoundPlacementGroup(
            client=mock.MagicMock(), data=placement_group_response["placement_group"]
        )

        check_variables(
            bound_placement_group, placement_group_response["placement_group"]
        )

    def test_update(
        self,
        request_mock: mock.MagicMock,
        bound_placement_group,
        placement_group_response,
    ):
        request_mock.return_value = placement_group_response

        placement_group = bound_placement_group.update(
            name=placement_group_response["placement_group"]["name"],
            labels=placement_group_response["placement_group"]["labels"],
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group_response["placement_group"]["id"]
            ),
            json={
                "labels": placement_group_response["placement_group"]["labels"],
                "name": placement_group_response["placement_group"]["name"],
            },
        )

        check_variables(placement_group, placement_group_response["placement_group"])

    def test_delete(
        self,
        request_mock: mock.MagicMock,
        bound_placement_group,
    ):
        delete_success = bound_placement_group.delete()

        request_mock.assert_called_with(
            method="DELETE",
            url="/placement_groups/897",
        )

        assert delete_success is True


class TestPlacementGroupsClient:
    @pytest.fixture()
    def placement_groups_client(self, client: Client):
        return PlacementGroupsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        placement_groups_client: PlacementGroupsClient,
        placement_group_response,
    ):
        request_mock.return_value = placement_group_response

        placement_group = placement_groups_client.get_by_id(
            placement_group_response["placement_group"]["id"]
        )

        request_mock.assert_called_with(
            method="GET",
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group_response["placement_group"]["id"]
            ),
        )

        assert placement_group._client is placement_groups_client

        check_variables(placement_group, placement_group_response["placement_group"])

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "my Placement Group",
                "sort": "id",
                "label_selector": "key==value",
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
        placement_groups_client: PlacementGroupsClient,
        two_placement_groups_response,
        params,
    ):
        request_mock.return_value = two_placement_groups_response

        result = placement_groups_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/placement_groups",
            params=params,
        )

        placement_groups = result.placement_groups
        assert result.meta is not None

        assert len(placement_groups) == len(
            two_placement_groups_response["placement_groups"]
        )

        for placement_group, expected in zip(
            placement_groups, two_placement_groups_response["placement_groups"]
        ):
            assert placement_group._client is placement_groups_client

            check_variables(placement_group, expected)

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "Corporate Intranet Protection",
                "sort": "id",
                "label_selector": "key==value",
            },
            {},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        placement_groups_client: PlacementGroupsClient,
        two_placement_groups_response,
        params,
    ):
        request_mock.return_value = two_placement_groups_response

        placement_groups = placement_groups_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/placement_groups",
            params=params,
        )

        assert len(placement_groups) == len(
            two_placement_groups_response["placement_groups"]
        )

        for placement_group, expected in zip(
            placement_groups, two_placement_groups_response["placement_groups"]
        ):
            assert placement_group._client is placement_groups_client

            check_variables(placement_group, expected)

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        placement_groups_client: PlacementGroupsClient,
        one_placement_group_response,
    ):
        request_mock.return_value = one_placement_group_response

        placement_group = placement_groups_client.get_by_name(
            one_placement_group_response["placement_groups"][0]["name"]
        )

        params = {"name": one_placement_group_response["placement_groups"][0]["name"]}

        request_mock.assert_called_with(
            method="GET",
            url="/placement_groups",
            params=params,
        )

        check_variables(
            placement_group, one_placement_group_response["placement_groups"][0]
        )

    def test_create(
        self,
        request_mock: mock.MagicMock,
        placement_groups_client: PlacementGroupsClient,
        response_create_placement_group,
    ):
        request_mock.return_value = response_create_placement_group

        response = placement_groups_client.create(
            name=response_create_placement_group["placement_group"]["name"],
            type=response_create_placement_group["placement_group"]["type"],
            labels=response_create_placement_group["placement_group"]["labels"],
        )

        json = {
            "name": response_create_placement_group["placement_group"]["name"],
            "labels": response_create_placement_group["placement_group"]["labels"],
            "type": response_create_placement_group["placement_group"]["type"],
        }

        request_mock.assert_called_with(
            method="POST",
            url="/placement_groups",
            json=json,
        )

        bound_placement_group = response.placement_group

        assert bound_placement_group._client is placement_groups_client
        check_variables(
            bound_placement_group, response_create_placement_group["placement_group"]
        )
