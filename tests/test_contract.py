import responses
from python_ise import ERS
from tests.helpers import load_fixture

BASE = "https://ise.test.invalid:9060/ers/config/endpoint"
OID = "abcd1234-ef56-7890-abcd1234ef56"

@responses.activate
def test_get_object_returns_result_contract(ers_client):
    responses.add(
        responses.GET,
        f"{BASE}/{OID}",
        json=load_fixture("ers/endpoint_by_id.json"),
        status=200,
    )
    result = ers_client._get_object(BASE, OID, "ERSEndPoint")
    assert result == {
        "success": True,
        "response": {"id": OID, "name": "aa:bb:cc:12:34:56"},
        "error": "",
    }

@responses.activate
def test_get_object_reports_429(ers_client):
    responses.add(
        responses.GET,
        f"{BASE}/{OID}",
        json={"message": "slow down"},
        status=429,
    )
    result = ers_client._get_object(BASE, OID, "ERSEndPoint")
    assert result["success"] is False
    assert result["error"] == 429
