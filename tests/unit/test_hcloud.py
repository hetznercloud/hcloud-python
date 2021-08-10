#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from unittest.mock import MagicMock

import requests
import pytest
from hcloud import Client, APIException


class TestHetznerClient(object):
    @pytest.fixture()
    def client(self):
        Client._version = "0.0.0"
        client = Client(token="project_token")

        client._requests_session = MagicMock()
        return client

    @pytest.fixture()
    def response(self):
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({"result": "data"}).encode("utf-8")
        return response

    @pytest.fixture()
    def fail_response(self, response):
        response.status_code = 422
        error = {
            "code": "invalid_input",
            "message": "invalid input in field 'broken_field': is too long",
            "details": {
                "fields": [{"name": "broken_field", "messages": ["is too long"]}]
            },
        }
        response._content = json.dumps({"error": error}).encode("utf-8")
        return response

    @pytest.fixture()
    def rate_limit_response(self, response):
        response.status_code = 422
        error = {
            "code": "rate_limit_exceeded",
            "message": "limit of 10 requests per hour reached",
            "details": {},
        }
        response._content = json.dumps({"error": error}).encode("utf-8")
        return response

    def test__get_user_agent(self, client):
        user_agent = client._get_user_agent()
        assert user_agent == "hcloud-python/0.0.0"

    def test__get_user_agent_with_application_name(self, client):
        client = Client(token="project_token", application_name="my-app")
        user_agent = client._get_user_agent()
        assert user_agent == "my-app hcloud-python/0.0.0"

    def test__get_user_agent_with_application_name_and_version(self, client):
        client = Client(
            token="project_token",
            application_name="my-app",
            application_version="1.0.0",
        )
        user_agent = client._get_user_agent()
        assert user_agent == "my-app/1.0.0 hcloud-python/0.0.0"

    def test__get_headers(self, client):
        headers = client._get_headers()
        assert headers == {
            "User-Agent": "hcloud-python/0.0.0",
            "Authorization": "Bearer project_token",
        }

    def test_request_library_mocked(self, client):
        response = client.request("POST", "url", params={"1": 2})
        assert response.__class__.__name__ == "MagicMock"

    def test_request_ok(self, client, response):
        client._requests_session.request.return_value = response
        response = client.request(
            "POST", "/servers", params={"argument": "value"}, timeout=2
        )
        client._requests_session.request.assert_called_once()
        assert client._requests_session.request.call_args[0] == (
            "POST",
            "https://api.hetzner.cloud/v1/servers",
        )
        assert client._requests_session.request.call_args[1]["params"] == {
            "argument": "value"
        }
        assert client._requests_session.request.call_args[1]["timeout"] == 2
        assert response == {"result": "data"}

    def test_request_fails(self, client, fail_response):
        client._requests_session.request.return_value = fail_response
        with pytest.raises(APIException) as exception_info:
            client.request(
                "POST", "http://url.com", params={"argument": "value"}, timeout=2
            )
        error = exception_info.value
        assert error.code == "invalid_input"
        assert error.message == "invalid input in field 'broken_field': is too long"
        assert error.details["fields"][0]["name"] == "broken_field"

    def test_request_500(self, client, fail_response):
        fail_response.status_code = 500
        fail_response.reason = "Internal Server Error"
        fail_response._content = "Internal Server Error"
        client._requests_session.request.return_value = fail_response
        with pytest.raises(APIException) as exception_info:
            client.request(
                "POST", "http://url.com", params={"argument": "value"}, timeout=2
            )
        error = exception_info.value
        assert error.code == 500
        assert error.message == "Internal Server Error"
        assert error.details["content"] == "Internal Server Error"

    def test_request_broken_json_200(self, client, response):
        content = "{'key': 'value'".encode("utf-8")
        response.reason = "OK"
        response._content = content
        client._requests_session.request.return_value = response
        with pytest.raises(APIException) as exception_info:
            client.request(
                "POST", "http://url.com", params={"argument": "value"}, timeout=2
            )
        error = exception_info.value
        assert error.code == 200
        assert error.message == "OK"
        assert error.details["content"] == content

    def test_request_empty_content_200(self, client, response):
        content = ""
        response.reason = "OK"
        response._content = content
        client._requests_session.request.return_value = response
        response = client.request(
            "POST", "http://url.com", params={"argument": "value"}, timeout=2
        )
        assert response == ""

    def test_request_500_empty_content(self, client, fail_response):
        fail_response.status_code = 500
        fail_response.reason = "Internal Server Error"
        fail_response._content = ""
        client._requests_session.request.return_value = fail_response
        with pytest.raises(APIException) as exception_info:
            client.request(
                "POST", "http://url.com", params={"argument": "value"}, timeout=2
            )
        error = exception_info.value
        assert error.code == 500
        assert error.message == "Internal Server Error"
        assert error.details["content"] == ""
        assert str(error) == "Internal Server Error"

    def test_request_limit(self, client, rate_limit_response):
        client._retry_wait_time = 0
        client._requests_session.request.return_value = rate_limit_response
        with pytest.raises(APIException) as exception_info:
            client.request(
                "POST", "http://url.com", params={"argument": "value"}, timeout=2
            )
        error = exception_info.value
        assert client._requests_session.request.call_count == 5
        assert error.code == "rate_limit_exceeded"
        assert error.message == "limit of 10 requests per hour reached"

    def test_request_limit_then_success(self, client, rate_limit_response):
        client._retry_wait_time = 0
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({"result": "data"}).encode("utf-8")
        client._requests_session.request.side_effect = [rate_limit_response, response]

        client.request(
            "POST", "http://url.com", params={"argument": "value"}, timeout=2
        )
        assert client._requests_session.request.call_count == 2
