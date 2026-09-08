from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.images import BoundImage, Image, ImagesClient
from hcloud.servers import BoundServer

from ..conftest import BoundModelTestCase, assert_bound_action1


def assert_bound_image1(
    o: BoundImage,
    client: ImagesClient,
):
    assert isinstance(o, BoundImage)
    assert o._client is client
    assert o.id == 45557056


def assert_bound_image2(
    o: BoundImage,
    client: ImagesClient,
):
    assert isinstance(o, BoundImage)
    assert o._client is client
    assert o.id == 429564329


class TestBoundImage(BoundModelTestCase):
    methods = [
        BoundImage.update,
        BoundImage.delete,
        BoundImage.change_protection,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.images

    @pytest.fixture()
    def bound_model(self, resource_client, image1):
        return BoundImage(resource_client, data=image1)

    def test_init(self, image1, image2):
        o = BoundImage(client=mock.MagicMock(), data=image1)

        assert o.id == 45557056
        assert o.type == "system"
        assert o.name == "debian-11"
        assert o.architecture == "x86"
        assert o.status == "available"
        assert o.description == "Debian 11"
        assert o.image_size is None
        assert o.disk_size == 5
        assert o.created == isoparse("2021-08-16T11:12:01Z")
        assert o.created_from is None
        assert o.bound_to is None
        assert o.os_flavor == "debian"
        assert o.os_version == "11"
        assert o.rapid_deploy is True
        assert o.labels == {}
        assert o.protection == {"delete": False}
        with pytest.deprecated_call():
            assert o.deprecated == isoparse("2026-08-31T06:21:44Z")
        assert o.deprecation.announced == isoparse("2026-08-31T06:21:44Z")
        assert o.deprecation.unavailable_after == isoparse("2026-12-01T00:00:00Z")

        o = BoundImage(client=mock.MagicMock(), data=image2)

        assert o.id == 429564329
        assert o.type == "snapshot"
        assert o.name is None
        assert o.architecture == "x86"
        assert o.status == "available"
        assert o.description == "snapshot 2026-09-08T13:44:08Z"
        assert o.image_size == 0.7237785009765625
        assert o.disk_size == 80
        assert o.created == isoparse("2026-09-08T13:44:08Z")
        assert isinstance(o.created_from, BoundServer)
        assert o.created_from.id == 159969127
        assert o.created_from.name == "server1"
        assert isinstance(o.bound_to, BoundServer)
        assert o.bound_to.id == 159969127
        assert o.os_flavor == "debian"
        assert o.os_version == "13"
        assert o.rapid_deploy is False
        assert o.labels == {"key": "value"}
        assert o.protection == {"delete": True}
        with pytest.deprecated_call():
            assert o.deprecated is None
        assert o.deprecation is None


class TestImagesClient:
    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.images

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image1,
    ):
        request_mock.return_value = {"image": image1}

        result = resource_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/images/1",
        )

        assert_bound_image1(result, resource_client)

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
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image1,
        image2,
        params,
    ):
        request_mock.return_value = {"images": [image1, image2]}

        result = resource_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/images",
            params=params,
        )

        assert result.meta is not None
        assert len(result.images) == 2

        assert_bound_image1(result.images[0], resource_client)
        assert_bound_image2(result.images[1], resource_client)

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
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image1,
        image2,
        params,
    ):
        request_mock.return_value = {"images": [image1, image2]}

        result = resource_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/images",
            params=params,
        )

        assert len(result) == 2
        assert_bound_image1(result[0], resource_client)
        assert_bound_image2(result[1], resource_client)

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image1,
    ):
        request_mock.return_value = {"images": [image1]}

        with pytest.deprecated_call():
            result = resource_client.get_by_name("debian-11")

        request_mock.assert_called_with(
            method="GET",
            url="/images",
            params={"name": "debian-11"},
        )

        assert_bound_image1(result, resource_client)

    def test_get_by_name_and_architecture(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image1,
    ):
        request_mock.return_value = {"images": [image1]}

        result = resource_client.get_by_name_and_architecture("debian-11", "x86")

        request_mock.assert_called_with(
            method="GET",
            url="/images",
            params={"name": "debian-11", "architecture": ["x86"]},
        )

        assert_bound_image1(result, resource_client)

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image,
        image1,
    ):
        request_mock.return_value = {"image": image1}

        image = resource_client.update(
            image,
            description="My new Image description",
            type="snapshot",
            labels={},
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/images/1",
            json={
                "description": "My new Image description",
                "type": "snapshot",
                "labels": {},
            },
        )

        assert_bound_image1(image, resource_client)

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image,
        action1_running,
    ):
        request_mock.return_value = {"action": action1_running}

        action = resource_client.change_protection(image, True)

        request_mock.assert_called_with(
            method="POST",
            url="/images/1/actions/change_protection",
            json={
                "delete": True,
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        resource_client: ImagesClient,
        image,
    ):
        request_mock.return_value = {}

        result = resource_client.delete(image)

        request_mock.assert_called_with(
            method="DELETE",
            url="/images/1",
        )

        assert result is True
