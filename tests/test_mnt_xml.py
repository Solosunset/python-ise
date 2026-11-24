from pathlib import Path

import responses

from python_ise import MNT

FIXTURES = Path(__file__).parent / "fixtures" / "mnt"
ACTIVE_LIST_URL = "https://ise.test.invalid/admin/API/mnt/Session/ActiveList"
AUTH_LIST_URL = "https://ise.test.invalid/admin/API/mnt/Session/AuthList/null/null"
EMPTY_ACTIVE_LIST = '<?xml version="1.0" encoding="UTF-8"?><activeList noOfActiveSession="0"/>'


def _mnt_client() -> MNT:
    return MNT(
        mnt_node="ise.test.invalid",
        mnt_user="u",
        mnt_pass="p",
        disable_warnings=True,
    )


def test_other_attr_string_repeated_key_becomes_list():
    assert MNT._other_attr_string_reader("a=1:!:a=2:!:")["a"] == ["1", "2"]


def test_response_reader_handles_repeated_av_pairs():
    assert MNT._response_reader("{a=1; a=2 }")["a"] == ["1", "2"]


def test_response_reader_ignores_trailing_semicolon():
    assert MNT._response_reader("{a=1; a=2; }") == {"a": ["1", "2"]}


@responses.activate
def test_active_list_single_and_many_shapes():
    responses.add(
        responses.GET,
        ACTIVE_LIST_URL,
        body=(FIXTURES / "active_list_single.xml").read_text(),
        status=200,
        content_type="application/xml",
    )
    responses.add(
        responses.GET,
        ACTIVE_LIST_URL,
        body=(FIXTURES / "active_list_many.xml").read_text(),
        status=200,
        content_type="application/xml",
    )

    client = _mnt_client()
    single = client.get_activeSessionList()
    many = client.get_activeSessionList()

    assert single["success"] is True
    assert single["error"] == ""
    assert isinstance(single["response"], list)
    assert len(single["response"]) == 1
    assert single["response"][0]["mac"] == "AA:BB:CC:00:11:22"

    assert many["success"] is True
    assert many["error"] == ""
    assert isinstance(many["response"], list)
    assert len(many["response"]) == 2
    assert all(isinstance(session, dict) for session in many["response"])


@responses.activate
def test_active_session_list_empty_returns_empty_list():
    responses.add(
        responses.GET,
        ACTIVE_LIST_URL,
        body=EMPTY_ACTIVE_LIST,
        status=200,
        content_type="application/xml",
    )

    result = _mnt_client().get_activeSessionList()

    assert result["success"] is True
    assert result["response"] == []


@responses.activate
def test_authenticated_sessions_list_empty_returns_empty_list():
    responses.add(
        responses.GET,
        AUTH_LIST_URL,
        body=EMPTY_ACTIVE_LIST,
        status=200,
        content_type="application/xml",
    )

    result = _mnt_client().get_authenticatedSessionsList()

    assert result["success"] is True
    assert result["response"] == []
