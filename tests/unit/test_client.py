from __future__ import annotations

from http import HTTPStatus
from json import dumps
from typing import Any
from unittest import mock

import pytest
import requests

from hcloud import (
    APIException,
    Client,
    constant_backoff_function,
    exponential_backoff_function,
)
from hcloud._client import ClientBase, _build_user_agent


def test_exponential_backoff_function():
    backoff = exponential_backoff_function(
        base=1.0,
        multiplier=2,
        cap=60.0,
    )
    max_retries = 5

    results = [backoff(i) for i in range(max_retries)]
    assert sum(results) == 31.0
    assert results == [1.0, 2.0, 4.0, 8.0, 16.0]


def test_constant_backoff_function():
    backoff = constant_backoff_function(interval=1.0)
    max_retries = 5

    for i in range(max_retries):
        assert backoff(i) == 1.0


def test_build_user_agent():
    assert _build_user_agent(None, None) == "hcloud-python/0.0.0"
    assert _build_user_agent("my-app", None) == "my-app hcloud-python/0.0.0"
    assert _build_user_agent("my-app", "1.0.0") == "my-app/1.0.0 hcloud-python/0.0.0"
    assert _build_user_agent(None, "1.0.0") == "hcloud-python/0.0.0"


class TestClient:
    @pytest.fixture()
    def client(self):
        return Client(token="TOKEN")

    def test_request(self, client: Client):
        client._client.request = mock.MagicMock()
        client.request(method="GET", url="/path")
        client._client.request.assert_called_once_with("GET", "/path")


def make_response(
    status: HTTPStatus,
    *,
    json: Any | None = None,
    text: str | None = None,
) -> requests.Response:
    response = requests.Response()
    response.status_code = status.value
    response.reason = status.phrase

    if json is not None:
        response.headers["Content-type"] = "application/json"
        response._content = dumps(json).encode("utf-8")
    elif text is not None:
        response.headers["Content-type"] = "text/plain"
        response._content = text.encode("utf-8")
    return response


class TestBaseClient:
    @pytest.fixture()
    def client(self):
        client = ClientBase(
            token="TOKEN",
            endpoint="https://api.hetzner.cloud/v1",
        )
        client._session = mock.MagicMock()
        return client

    def test_init(self, client: ClientBase):
        assert client._user_agent == "hcloud-python/0.0.0"
        assert client._headers == {
            "User-Agent": "hcloud-python/0.0.0",
            "Authorization": "Bearer TOKEN",
            "Accept": "application/json",
        }
        assert client._poll_interval_func(1) == 1.0
        assert client._retry_interval_func(1) == pytest.approx(1.5, rel=0.5)  # Jitter

    @pytest.mark.parametrize(
        ("exception", "expected"),
        [
            (
                APIException(code="rate_limit_exceeded", message="Error", details=None),
                True,
            ),
            (
                APIException(code="conflict", message="Error", details=None),
                True,
            ),
            (
                APIException(code=409, message="Conflict", details=None),
                False,
            ),
            (
                APIException(code=429, message="Too Many Requests", details=None),
                False,
            ),
            (
                APIException(code=502, message="Bad Gateway", details=None),
                True,
            ),
            (
                APIException(code=503, message="Service Unavailable", details=None),
                False,
            ),
            (
                APIException(code=504, message="Gateway Timeout", details=None),
                True,
            ),
        ],
    )
    def test_retry_policy(
        self,
        client: ClientBase,
        exception: APIException,
        expected: bool,
    ):
        assert client._retry_policy(exception) == expected

    def test_request_200(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.OK,
            json={"result": "data"},
        )

        result = client.request(
            method="POST",
            url="/path",
            params={"argument": "value"},
            timeout=2,
        )

        client._session.request.assert_called_once_with(
            method="POST",
            url="https://api.hetzner.cloud/v1/path",
            headers={
                "User-Agent": "hcloud-python/0.0.0",
                "Authorization": "Bearer TOKEN",
                "Accept": "application/json",
            },
            params={"argument": "value"},
            timeout=2,
        )
        assert result == {"result": "data"}

    def test_request_200_empty_content(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.OK,
            text="",
        )

        result = client.request(method="POST", url="/path")
        assert result == {}

    def test_request_fail_200_invalid_json(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.OK,
            text="{'key': 'value'",
        )

        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert exc.value.code == 200
        assert exc.value.message == "OK"
        assert exc.value.details["content"] == b"{'key': 'value'"

    def test_request_fail_422(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
            json={
                "error": {
                    "code": "invalid_input",
                    "message": "invalid input in field 'broken_field': is too long",
                    "details": {
                        "fields": [
                            {"name": "broken_field", "messages": ["is too long"]}
                        ]
                    },
                }
            },
        )

        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert exc.value.code == "invalid_input"
        assert exc.value.message == "invalid input in field 'broken_field': is too long"
        assert exc.value.details["fields"][0]["name"] == "broken_field"

    def test_request_fail_422_correlation_id(self, client: ClientBase):
        response = make_response(
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
            json={
                "error": {
                    "code": "service_error",
                    "message": "Something crashed",
                }
            },
        )
        response.headers["X-Correlation-Id"] = "67ed842dc8bc8673"
        client._session.request.return_value = response

        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert exc.value.code == "service_error"
        assert exc.value.message == "Something crashed"
        assert exc.value.details is None
        assert exc.value.correlation_id == "67ed842dc8bc8673"
        assert str(exc.value) == "Something crashed (service_error, 67ed842dc8bc8673)"

    def test_request_fail_500(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            text="Internal Server Error",
        )

        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert exc.value.code == 500
        assert exc.value.message == "Internal Server Error"
        assert exc.value.details["content"] == b"Internal Server Error"

    def test_request_fail_500_no_content(self, client: ClientBase):
        client._session.request.return_value = make_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert exc.value.code == 500
        assert exc.value.message == "Internal Server Error"
        assert exc.value.details["content"] is None
        assert str(exc.value) == "Internal Server Error (500)"

    def test_request_fail_419(self, client: ClientBase):
        client._retry_interval_func = constant_backoff_function(0.0)

        client._session.request.return_value = make_response(
            status=HTTPStatus.TOO_MANY_REQUESTS,
            json={
                "error": {
                    "code": "rate_limit_exceeded",
                    "message": "limit of 3600 requests per hour reached",
                    "details": None,
                }
            },
        )
        with pytest.raises(APIException) as exc:
            client.request(method="POST", url="/path")

        assert client._session.request.call_count == 6
        assert exc.value.code == "rate_limit_exceeded"
        assert exc.value.message == "limit of 3600 requests per hour reached"

    def test_request_fail_419_recover(self, client: ClientBase):
        client._retry_interval_func = constant_backoff_function(0.0)

        client._session.request.side_effect = [
            make_response(
                status=HTTPStatus.TOO_MANY_REQUESTS,
                json={
                    "error": {
                        "code": "rate_limit_exceeded",
                        "message": "limit of 3600 requests per hour reached",
                        "details": None,
                    }
                },
            ),
            make_response(
                status=HTTPStatus.OK,
                json={"result": "data"},
            ),
        ]

        result = client.request(method="GET", url="/path")

        assert client._session.request.call_count == 2
        assert result == {"result": "data"}

    def test_request_fail_timeout(self, client: ClientBase):
        client._retry_interval_func = constant_backoff_function(0.0)
        client._session.request.side_effect = requests.exceptions.Timeout("timeout")

        with pytest.raises(requests.exceptions.Timeout) as exc:
            client.request(method="GET", url="/path")

        assert str(exc.value) == "timeout"
        assert client._session.request.call_count == 6

    def test_request_fail_timeout_recover(self, client: ClientBase):
        client._retry_interval_func = constant_backoff_function(0.0)

        client._session.request.side_effect = [
            requests.exceptions.Timeout("timeout"),
            make_response(
                status=HTTPStatus.OK,
                json={"result": "data"},
            ),
        ]

        result = client.request(method="GET", url="/path")

        assert client._session.request.call_count == 2
        assert result == {"result": "data"}
