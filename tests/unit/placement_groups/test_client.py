from __future__ import annotations

from unittest import mock

import pytest

from hcloud.placement_groups import BoundPlacementGroup, PlacementGroupsClient


def check_variables(placement_group, expected):
    assert placement_group.id == expected["id"]
    assert placement_group.name == expected["name"]
    assert placement_group.labels == expected["labels"]
    assert placement_group.servers == expected["servers"]
    assert placement_group.type == expected["type"]


class TestBoundPlacementGroup:
    @pytest.fixture()
    def bound_placement_group(self, hetzner_client):
        return BoundPlacementGroup(
            client=hetzner_client.placement_groups, data=dict(id=897)
        )

    def test_bound_placement_group_init(self, placement_group_response):
        bound_placement_group = BoundPlacementGroup(
            client=mock.MagicMock(), data=placement_group_response["placement_group"]
        )

        check_variables(
            bound_placement_group, placement_group_response["placement_group"]
        )

    def test_update(
        self, hetzner_client, bound_placement_group, placement_group_response
    ):
        hetzner_client.request.return_value = placement_group_response
        placement_group = bound_placement_group.update(
            name=placement_group_response["placement_group"]["name"],
            labels=placement_group_response["placement_group"]["labels"],
        )
        hetzner_client.request.assert_called_with(
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group_response["placement_group"]["id"]
            ),
            method="PUT",
            json={
                "labels": placement_group_response["placement_group"]["labels"],
                "name": placement_group_response["placement_group"]["name"],
            },
        )

        check_variables(placement_group, placement_group_response["placement_group"])

    def test_delete(self, hetzner_client, bound_placement_group):
        delete_success = bound_placement_group.delete()
        hetzner_client.request.assert_called_with(
            url="/placement_groups/897", method="DELETE"
        )

        assert delete_success is True


class TestPlacementGroupsClient:
    @pytest.fixture()
    def placement_groups_client(self):
        return PlacementGroupsClient(client=mock.MagicMock())

    def test_get_by_id(self, placement_groups_client, placement_group_response):
        placement_groups_client._client.request.return_value = placement_group_response
        placement_group = placement_groups_client.get_by_id(
            placement_group_response["placement_group"]["id"]
        )
        placement_groups_client._client.request.assert_called_with(
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group_response["placement_group"]["id"]
            ),
            method="GET",
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
        self, placement_groups_client, two_placement_groups_response, params
    ):
        placement_groups_client._client.request.return_value = (
            two_placement_groups_response
        )
        result = placement_groups_client.get_list(**params)
        placement_groups_client._client.request.assert_called_with(
            url="/placement_groups", method="GET", params=params
        )

        placement_groups = result.placement_groups
        assert result.meta is None

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
        self, placement_groups_client, two_placement_groups_response, params
    ):
        placement_groups_client._client.request.return_value = (
            two_placement_groups_response
        )
        placement_groups = placement_groups_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})
        placement_groups_client._client.request.assert_called_with(
            url="/placement_groups", method="GET", params=params
        )

        assert len(placement_groups) == len(
            two_placement_groups_response["placement_groups"]
        )

        for placement_group, expected in zip(
            placement_groups, two_placement_groups_response["placement_groups"]
        ):
            assert placement_group._client is placement_groups_client

            check_variables(placement_group, expected)

    def test_get_by_name(self, placement_groups_client, one_placement_group_response):
        placement_groups_client._client.request.return_value = (
            one_placement_group_response
        )
        placement_group = placement_groups_client.get_by_name(
            one_placement_group_response["placement_groups"][0]["name"]
        )

        params = {"name": one_placement_group_response["placement_groups"][0]["name"]}
        placement_groups_client._client.request.assert_called_with(
            url="/placement_groups", method="GET", params=params
        )

        check_variables(
            placement_group, one_placement_group_response["placement_groups"][0]
        )

    def test_create(self, placement_groups_client, response_create_placement_group):
        placement_groups_client._client.request.return_value = (
            response_create_placement_group
        )
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
        placement_groups_client._client.request.assert_called_with(
            url="/placement_groups", method="POST", json=json
        )

        bound_placement_group = response.placement_group

        assert bound_placement_group._client is placement_groups_client
        check_variables(
            bound_placement_group, response_create_placement_group["placement_group"]
        )
