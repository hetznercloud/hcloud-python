import mock
import pytest

from hcloud.images.client import BoundImage
from hcloud.images.domain import Image


class TestBoundImage(object):
    @pytest.fixture()
    def bound_image(self, hetzner_client):
        return BoundImage(client=hetzner_client.images, data=dict(id=42))

    def test_get_actions_list(self, bound_image):
        result = bound_image.get_actions_list()
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    def test_update(self, bound_image):
        image = bound_image.update(description="My new Image description", type="snapshot", labels={})

        assert image.id == 4711
        assert image.description == "My new Image description"

    def test_delete(self, bound_image):
        delete_success = bound_image.delete()

        assert delete_success is True

    def test_change_protection(self, bound_image):
        action = bound_image.change_protection(True)

        assert action.id == 13
        assert action.command == "change_protection"


class TestImagesClient(object):
    def test_get_by_id(self, hetzner_client):
        image = hetzner_client.images.get_by_id(1)
        assert image.id == 4711
        assert image.name == "ubuntu-20.04"
        assert image.description == "Ubuntu 20.04 Standard 64 bit"

    def test_get_by_name(self, hetzner_client):
        image = hetzner_client.images.get_by_name("ubuntu-20.04")
        assert image.id == 4711
        assert image.name == "ubuntu-20.04"
        assert image.description == "Ubuntu 20.04 Standard 64 bit"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.images.get_list()
        images = result.images
        assert images[0].id == 4711
        assert images[0].name == "ubuntu-20.04"
        assert images[0].description == "Ubuntu 20.04 Standard 64 bit"

    @pytest.mark.parametrize("image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))])
    def test_get_actions_list(self, hetzner_client, image):
        result = hetzner_client.images.get_actions_list(image)
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "change_protection"

    @pytest.mark.parametrize("image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, image):
        image = hetzner_client.images.update(image, description="My new Image description", type="snapshot", labels={})

        assert image.id == 4711
        assert image.description == "My new Image description"

    @pytest.mark.parametrize("image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, image):
        delete_success = hetzner_client.images.delete(image)

        assert delete_success is True

    @pytest.mark.parametrize("image", [Image(id=1), BoundImage(mock.MagicMock(), dict(id=1))])
    def test_change_protection(self, hetzner_client, image):
        action = hetzner_client.images.change_protection(image, delete=True)

        assert action.id == 13
        assert action.command == "change_protection"
