import asyncio
from datetime import datetime, timedelta

import aiohttp
import responses
from aioresponses import aioresponses

BASE = "https://ise.test.invalid:9060/ers/config/endpoint"
VERSION_URL = "https://ise.test.invalid:9060/ers/config/deploymentinfo/versioninfo"
FIXED_NOW = datetime(2026, 1, 1, 12, 0, 0)


def _calls_to(url):
    return [call for call in responses.calls if call.request.url == url]


@responses.activate
def test_csrf_token_is_fetched_once_and_reused(ers_client):
    ers_client.use_csrf = True
    ers_client.clock = lambda: FIXED_NOW
    responses.add(
        responses.GET,
        VERSION_URL,
        headers={"X-CSRF-Token": "csrf-1"},
        json={},
        status=200,
    )
    first_url = f"{BASE}/first"
    second_url = f"{BASE}/second"
    for url in (first_url, second_url):
        responses.add(responses.GET, url, json={"ERSEndPoint": {"id": url}}, status=200)

    ers_client._request(first_url)
    ers_client._request(second_url)

    version_calls = _calls_to(VERSION_URL)
    assert len(version_calls) == 1
    assert version_calls[0].request.headers["X-CSRF-TOKEN"] == "fetch"
    data_calls = _calls_to(first_url) + _calls_to(second_url)
    assert [call.request.headers["X-CSRF-TOKEN"] for call in data_calls] == [
        "csrf-1",
        "csrf-1",
    ]
    assert ers_client.csrf_expires == FIXED_NOW + timedelta(seconds=60)


@responses.activate
def test_csrf_token_is_refetched_when_injected_clock_expires(ers_client):
    ers_client.use_csrf = True
    now = [FIXED_NOW]
    ers_client.clock = lambda: now[0]
    responses.add(
        responses.GET,
        VERSION_URL,
        headers={"X-CSRF-Token": "csrf-1"},
        json={},
        status=200,
    )
    responses.add(
        responses.GET,
        VERSION_URL,
        headers={"X-CSRF-Token": "csrf-2"},
        json={},
        status=200,
    )
    first_url = f"{BASE}/first"
    second_url = f"{BASE}/second"
    for url in (first_url, second_url):
        responses.add(responses.GET, url, json={"ERSEndPoint": {"id": url}}, status=200)

    ers_client._request(first_url)
    now[0] = FIXED_NOW + timedelta(seconds=61)
    ers_client._request(second_url)

    version_calls = _calls_to(VERSION_URL)
    assert len(version_calls) == 2
    data_calls = _calls_to(first_url) + _calls_to(second_url)
    assert [call.request.headers["X-CSRF-TOKEN"] for call in data_calls] == [
        "csrf-1",
        "csrf-2",
    ]


@responses.activate
def test_rate_limit_result_shape(ers_client):
    responses.add(
        responses.GET,
        f"{BASE}/x",
        json={"message": "slow down"},
        status=429,
    )

    result = ers_client._get_object(BASE, "x", "ERSEndPoint")

    assert result["success"] is False
    assert result["error"] == 429
    assert set(result) == {"success", "response", "error"}
    assert isinstance(result["response"], str)
    assert "Too Many Requests (ratelimit)" in result["response"]
    assert "slow down" in result["response"]


@responses.activate
def test_rate_limit_plain_text_body_still_returns_result_contract(ers_client):
    responses.add(
        responses.GET,
        f"{BASE}/x",
        body="slow down",
        status=429,
    )

    result = ers_client._get_object(BASE, "x", "ERSEndPoint")

    assert result["success"] is False
    assert result["error"] == 429
    assert set(result) == {"success", "response", "error"}
    assert "Too Many Requests (ratelimit)" in result["response"]
    assert "slow down" in result["response"]


def test_async_path_uses_same_auth_and_accept_headers(ers_client):
    original_headers = dict(ers_client.ise.headers)
    payload = {
        "SearchResult": {
            "total": 1,
            "resources": [{"name": "aa:bb:cc:12:34:56", "id": "endpoint-id"}],
        }
    }

    async def call():
        async with aiohttp.ClientSession() as session:
            return await ers_client._async_get_objects(
                session, BASE, {"size": 20, "page": 1}
            )

    with aioresponses() as mocked:
        mocked.get(BASE + "?page=1&size=20", payload=payload)
        result = asyncio.run(call())
        captured = [
            call
            for (method, _), calls in mocked.requests.items()
            if method == "GET"
            for call in calls
        ]

    assert len(captured) == 1
    auth = captured[0].kwargs["auth"]
    assert auth.login == ers_client.user_name
    assert auth.password == ers_client.user_pass
    headers = captured[0].kwargs["headers"]
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert ers_client.ise.headers == original_headers
    assert result["success"] is True
