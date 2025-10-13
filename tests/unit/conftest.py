# pylint: disable=redefined-outer-name

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import ClassVar, TypedDict
from unittest import mock

import pytest

from hcloud import Client
from hcloud.actions import ActionsClient, BoundAction


@pytest.fixture(autouse=True, scope="session")
def patch_package_version():
    with mock.patch("hcloud._client.__version__", "0.0.0"):
        yield


@pytest.fixture()
def request_mock() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture()
def client(request_mock) -> Client:
    c = Client(
        token="TOKEN",
        # Speed up tests that use `_poll_interval_func`
        poll_interval=0.0,
        poll_max_retries=3,
    )
    c._client.request = request_mock
    return c


def assert_bound_action1(o: BoundAction, client: ActionsClient):
    assert o.id == 1
    assert o.command == "command"
    assert o._client == client


def assert_bound_action2(o: BoundAction, client: ActionsClient):
    assert o.id == 2
    assert o.command == "command"
    assert o._client == client


@pytest.fixture()
def action1_running():
    return {
        "id": 1,
        "command": "command",
        "status": "running",
        "progress": 0,
        "started": "2016-01-30T23:50+00:00",
        "finished": None,
        "resources": [{"id": 42, "type": "resource"}],
        "error": None,
    }


@pytest.fixture()
def action2_running():
    return {
        "id": 2,
        "command": "command",
        "status": "running",
        "progress": 20,
        "started": "2016-01-30T23:50+00:00",
        "finished": None,
        "resources": [{"id": 43, "type": "resource"}],
        "error": None,
    }


@pytest.fixture()
def action1_success(action1_running):
    return {
        **action1_running,
        "status": "success",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
    }


@pytest.fixture()
def action2_success(action2_running):
    return {
        **action2_running,
        "status": "success",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
    }


@pytest.fixture()
def action1_error(action1_running):
    return {
        **action1_running,
        "status": "error",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
        "error": {"code": "action_failed", "message": "Action failed"},
    }


@pytest.fixture()
def action2_error(action2_running):
    return {
        **action2_running,
        "status": "error",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
        "error": {"code": "action_failed", "message": "Action failed"},
    }


@pytest.fixture()
def action_response(action1_running):
    return {
        "action": action1_running,
    }


@pytest.fixture()
def action_list_response(action1_running, action2_running):
    return {
        "actions": [
            action1_running,
            action2_running,
        ],
    }


def build_kwargs_mock(func: Callable) -> dict[str, mock.Mock]:
    """
    Generate a kwargs dict that may be passed to the provided function for testing purposes.
    """
    s = inspect.signature(func)

    kwargs = {}
    for name, param in s.parameters.items():
        if name in ("self",):
            continue

        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY):
            kwargs[name] = mock.Mock()
            continue

        # Ignore **kwargs
        if param.kind in (param.VAR_KEYWORD,):
            continue

        raise NotImplementedError(f"unsupported parameter kind: {param.kind}")

    return kwargs


def pytest_generate_tests(metafunc: pytest.Metafunc):
    """
    Magic function to generate a test for each bound model method.
    """
    if "bound_model_method" in metafunc.fixturenames:
        metafunc.parametrize("bound_model_method", metafunc.cls.methods)


class BoundModelTestOptions(TypedDict):
    sub_resource: bool


class BoundModelTestCase:
    methods: ClassVar[list[Callable | tuple[Callable, BoundModelTestOptions]]]

    def test_method_list(self, bound_model):
        """
        Ensure the list of bound model methods is up to date.
        """
        # Unpack methods
        methods = [m[0] if isinstance(m, tuple) else m for m in self.__class__.methods]

        members_count = 0
        members_missing = []
        for name, member in inspect.getmembers(
            bound_model,
            lambda m: inspect.ismethod(m)
            and m.__func__ in bound_model.__class__.__dict__.values(),
        ):
            # Actions methods are already tested in TestBoundModelActions.
            if name in ("__init__", "get_actions", "get_actions_list"):
                continue

            if member.__func__ in methods:
                members_count += 1
            else:
                members_missing.append(member.__func__.__qualname__)

        assert not members_missing, "untested methods:\n" + ",\n".join(members_missing)
        assert members_count == len(self.__class__.methods)

    def test_method(
        self,
        resource_client,
        bound_model,
        bound_model_method: Callable | tuple[Callable, BoundModelTestOptions],
    ):
        options = BoundModelTestOptions()
        if isinstance(bound_model_method, tuple):
            bound_model_method, options = bound_model_method

        # Check if the resource client has a method named after the bound model method.
        assert hasattr(resource_client, bound_model_method.__name__)

        # Mock the resource client method.
        resource_client_method_mock = mock.MagicMock()
        setattr(
            resource_client,
            bound_model_method.__name__,
            resource_client_method_mock,
        )

        kwargs = build_kwargs_mock(bound_model_method)

        # Call the bound model method
        result = getattr(bound_model, bound_model_method.__name__)(**kwargs)

        if options.get("sub_resource"):
            resource_client_method_mock.assert_called_with(**kwargs)
        else:
            resource_client_method_mock.assert_called_with(bound_model, **kwargs)

        assert result is resource_client_method_mock.return_value
