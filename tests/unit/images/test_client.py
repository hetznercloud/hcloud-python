from __future__ import annotations

import datetime
from datetime import timezone
from unittest import mock

import pytest

from hcloud.actions import BoundAction
from hcloud.images import BoundImage, Image, ImagesClient
from hcloud.servers import BoundServer


class TestBoundImage:
    @pytest.fixture()
    def bound_image(self, hetzner_client):
        return BoundImage(client=hetzner_client.images, data=dict(id=14))

    def test_bound_image_init(self, image_response):
        bound_image = BoundImage(client=mock.MagicMock(), data=image_response["image"])

        assert bound_image.id == 4711
        assert bound_image.type == "snapshot"
        assert bound_image.status == "available"
        assert bound_image.name == "ubuntu-20.04"
        assert bound_image.description == "Ubuntu 20.04 Standard 64 bit"
        assert bound_image.image_size == 2.3
        assert bound_image.disk_size == 10
        assert bound_image.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
        assert bound_image.os_flavor == "ubuntu"
        assert bound_image.os_version == "16.04"
        assert bound_image.architecture == "x86"
        assert bound_image.rapid_deploy is False
        assert bound_image.deprecated == datetime.datetime(
            2018, 2, 28, 0, 0, tzinfo=timezone.utc
        )

        assert isinstance(bound_image.created_from, BoundServer)
        assert bound_image.created_from.id == 1
        assert bound_image.created_from.name == "Server"
        assert bound_image.created_from.complete is False

        assert isinstance(bound_image.bound_to, BoundServer)
        assert bound_image.bound_to.id == 1
        assert bound_image.bound_to.complete is False

    @pytest.mark.parametrize(
        "params", [{}, {"sort": ["status"], "page": 1, "per_page": 2}]
    )
    def test_get_actions_list(
        self, hetzner_client, bound_image, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        result = bound_image.get_actions_list(**params)
        hetzner_client.request.assert_called_with(
            url="/images/14/actions", method="GET", params=params
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    @pytest.mark.parametrize("params", [{}, {"sort": ["status"]}])
    def test_get_actions(
        self, hetzner_client, bound_image, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_image.get_actions(**params)

        params.update({"page": 1, "per_page": 50})

        hetzner_client.request.assert_called_with(
            url="/images/14/actions", method="GET", params=params
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    def test_update(self, hetzner_client, bound_image, response_update_image):
        hetzner_client.request.return_value = response_update_image
        image = bound_image.update(
            description="My new Image description", type="snapshot", labels={}
        )
        hetzner_client.request.assert_called_with(
            url="/images/14",
            method="PUT",
            json={
                "description": "My new Image description",
                "type": "snapshot",
                "labels": {},
            },
        )

        assert image.id == 4711
        assert image.description == "My new Image description"

    def test_delete(self, hetzner_client, bound_image, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_image.delete()
        hetzner_client.request.assert_called_with(url="/images/14", method="DELETE")

        assert delete_success is True

    def test_change_protection(self, hetzner_client, bound_image, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_image.change_protection(True)
        hetzner_client.request.assert_called_with(
            url="/images/14/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0


class TestImagesClient:
    @pytest.fixture()
    def images_client(self):
        return ImagesClient(client=mock.MagicMock())

    def test_get_by_id(self, images_client, image_response):
        images_client._client.request.return_value = image_response
        image = images_client.get_by_id(1)
        images_client._client.request.assert_called_with(url="/images/1", method="GET")
        assert image._client is images_client
        assert image.id == 4711
        assert image.name == "ubuntu-20.04"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "ubuntu-20.04",
                "type": "system",
                "sort": "id",
                "bound_to": "1",
                "label_selector": "k==v",
                "page": 1,
                "per_page": 10,
            },
            {"name": ""},
            {"include_deprecated": True},
            {},
        ],
    )
    def test_get_list(self, images_client, two_images_response, params):
        images_client._client.request.return_value = two_images_response
        result = images_client.get_list(**params)
        images_client._client.request.assert_called_with(
            url="/images", method="GET", params=params
        )

        images = result.images
        assert result.meta is None

        assert len(images) == 2

        images1 = images[0]
        images2 = images[1]

        assert images1._client is images_client
        assert images1.id == 4711
        assert images1.name == "ubuntu-20.04"

        assert images2._client is images_client
        assert images2.id == 4712
        assert images2.name == "ubuntu-18.10"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "ubuntu-20.04",
                "type": "system",
                "sort": "id",
                "bound_to": "1",
                "label_selector": "k==v",
            },
            {"include_deprecated": True},
            {},
        ],
    )
    def test_get_all(self, images_client, two_images_response, params):
        images_client._client.request.return_value = two_images_response
        images = images_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        images_client._client.request.assert_called_with(
            url="/images", method="GET", params=params
        )

        assert len(images) == 2

        images1 = images[0]
        images2 = images[1]

        assert images1._client is images_client
        assert images1.id == 4711
        assert images1.name == "ubuntu-20.04"

        assert images2._client is images_client
        assert images2.id == 4712
        assert images2.name == "ubuntu-18.10"

    def test_get_by_name(self, images_client, one_images_response):
        images_client._client.request.return_value = one_images_response
        image = images_client.get_by_name("ubuntu-20.04")

        params = {"name": "ubuntu-20.04"}

        images_client._client.request.assert_called_with(
            url="/images", method="GET", params=params
        )

        assert image._client is images_client
        assert image.id == 4711
        assert image.name == "ubuntu-20.04"

    def test_get_by_name_and_architecture(self, images_client, one_images_response):
        images_client._client.request.return_value = one_images_response
        image = images_client.get_by_name_and_architecture("ubuntu-20.04", "x86")

        params = {"name": "ubuntu-20.04", "architecture": ["x86"]}

        images_client._client.request.assert_called_with(
            url="/images", method="GET", params=params
        )

        assert image._client is images_client
        assert image.id == 4711
        assert image.name == "ubuntu-20.04"
        assert image.architecture == "x86"

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_get_actions_list(self, images_client, image, response_get_actions):
        images_client._client.request.return_value = response_get_actions
        result = images_client.get_actions_list(image)
        images_client._client.request.assert_called_with(
            url="/images/1/actions", method="GET", params={}
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == images_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_update(self, images_client, image, response_update_image):
        images_client._client.request.return_value = response_update_image
        image = images_client.update(
            image, description="My new Image description", type="snapshot", labels={}
        )
        images_client._client.request.assert_called_with(
            url="/images/1",
            method="PUT",
            json={
                "description": "My new Image description",
                "type": "snapshot",
                "labels": {},
            },
        )

        assert image.id == 4711
        assert image.description == "My new Image description"

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, images_client, image, generic_action):
        images_client._client.request.return_value = generic_action
        action = images_client.change_protection(image, True)
        images_client._client.request.assert_called_with(
            url="/images/1/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, images_client, image, generic_action):
        images_client._client.request.return_value = generic_action
        delete_success = images_client.delete(image)
        images_client._client.request.assert_called_with(
            url="/images/1", method="DELETE"
        )

        assert delete_success is True

    def test_actions_get_by_id(self, images_client, response_get_actions):
        images_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = images_client.actions.get_by_id(13)

        images_client._client.request.assert_called_with(
            url="/images/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == images_client._client.actions
        assert action.id == 13
        assert action.command == "change_protection"

    def test_actions_get_list(self, images_client, response_get_actions):
        images_client._client.request.return_value = response_get_actions
        result = images_client.actions.get_list()

        images_client._client.request.assert_called_with(
            url="/images/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == images_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    def test_actions_get_all(self, images_client, response_get_actions):
        images_client._client.request.return_value = response_get_actions
        actions = images_client.actions.get_all()

        images_client._client.request.assert_called_with(
            url="/images/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == images_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"
