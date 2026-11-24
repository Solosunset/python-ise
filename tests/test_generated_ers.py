import ast
import inspect
from dataclasses import replace
from pathlib import Path

import pytest
import responses
from aioresponses import aioresponses

from python_ise import ERS, InvalidOID
from python_ise import generate as generate_module
from python_ise.generate import render
from python_ise.spec import load_specs
from tests.helpers import load_fixture

BASE = "https://ise.test.invalid:9060/ers/config/endpoint"
GROUP_BASE = "https://ise.test.invalid:9060/ers/config/endpointgroup"
OID = "abcd1234-ef56-7890-abcd1234ef56"
# The pinned fixture body id is 8-4-4-12, which the legacy _oid_test regex rejects.
# Use a valid 8-4-4-4-12 id for request URLs; the fixture body is left untouched.
VALID_OID = "abcd1234-ef56-7890-abcd-1234ef56abcd"
MANIFEST = Path("src/python_ise/manifest/ers.yaml")


def _load_generated_class(source: str):
    namespace = {}
    exec(compile(source, "ers_read.py", "exec"), namespace)
    return namespace["ERSGeneratedMethods"]


@responses.activate
def test_generated_by_id_uses_manifest_path_and_wrapper(ers_client):
    responses.add(
        responses.GET,
        f"{BASE}/{VALID_OID}",
        json=load_fixture("ers/endpoint_by_id.json"),
        status=200,
    )
    assert ERS.get_endpoint_id.__module__ == "python_ise.generated.ers_read"
    assert ers_client.get_endpoint_id(VALID_OID)["response"] == {
        "id": OID,
        "name": "aa:bb:cc:12:34:56",
    }


def test_generated_by_id_preserves_oid_validation(ers_client):
    with pytest.raises(InvalidOID):
        ers_client.get_endpoint_id("not-an-oid")


@responses.activate
def test_generated_by_id_passes_manifest_wrapper_key(ers_client, monkeypatch):
    fixture_key = next(iter(load_fixture("ers/endpoint_by_id.json")))
    captured = []

    def capture_wrapper(url, objectid, objecttype):
        captured.append(objecttype)
        return {"success": True, "response": {}, "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", capture_wrapper)
    ers_client.get_endpoint_id(VALID_OID)
    assert captured == [fixture_key]


@pytest.mark.parametrize(
    ("method_name", "expected_wrapper"),
    [
        ("get_byodPortal_id", "BYODPortal"),
        ("get_certificateTemplate_id", "ERSCertificateTemplate"),
        ("get_certificateTemplate_name", "ERSCertificateTemplate"),
        ("get_guestSmtpNotificationSetting_id", "ERSGuestSmtpNotificationSettings"),
        ("get_identity_group_id", "IdentityGroup"),
        ("get_identity_group_name", "IdentityGroup"),
        ("get_nspProfile_id", "ERSNSPProfile"),
        ("get_portal_id", "ERSPortal"),
        ("get_portalGlobalSetting_id", "PortalCustomizationGlobalSetting"),
        ("get_tacacsCommandSet_id", "TacacsCommandSets"),
    ],
)
def test_generated_by_key_uses_live_observed_wrapper(
    ers_client, monkeypatch, method_name, expected_wrapper
):
    captured = []

    def capture_wrapper(url, objectid, objecttype):
        captured.append(objecttype)
        return {"success": True, "response": {}, "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", capture_wrapper)
    getattr(ers_client, method_name)(VALID_OID)

    assert captured == [expected_wrapper]


def test_wrong_manifest_wrapper_key_is_rejected(tmp_path, ers_client, monkeypatch):
    wrong_manifest = tmp_path / "ers.yaml"
    wrong_manifest.write_text(
        MANIFEST.read_text().replace(
            'wrapper: "ERSEndPoint"', 'wrapper: "WrongWrapper"'
        )
    )
    generated_cls = _load_generated_class(render(load_specs(wrong_manifest)))
    fixture_key = next(iter(load_fixture("ers/endpoint_by_id.json")))

    def strict_get_object(url, objectid, objecttype):
        assert objecttype == fixture_key, (
            f"generated wrapper {objecttype!r} != fixture key {fixture_key!r}"
        )
        return {"success": True, "response": {}, "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", strict_get_object)
    with pytest.raises(AssertionError, match="WrongWrapper"):
        generated_cls.get_endpoint_id(ers_client, VALID_OID)


@responses.activate
def test_generated_version_info_uses_version_info_wrapper(ers_client):
    fixture = load_fixture("ers/endpoint_versioninfo.json")
    responses.add(responses.GET, f"{BASE}/versioninfo", json=fixture, status=200)
    assert ers_client.get_endpoint_versionInfo()["response"] == fixture["VersionInfo"]


@responses.activate
def test_generated_list_returns_search_result_shape(ers_client):
    responses.add(
        responses.GET, BASE, json=load_fixture("ers/endpoint_list.json"), status=200
    )
    result = ers_client.get_endpoints(size=100, page=1)
    assert result["success"] is True
    assert result["total"] == 1
    assert isinstance(result["response"], list)


@responses.activate
def test_generated_list_handles_empty_total(ers_client):
    responses.add(responses.GET, BASE, json={"SearchResult": {"total": 0}}, status=200)
    result = ers_client.get_endpoints(size=100, page=1)
    assert result["response"] == [] and result["success"] is True


@responses.activate
def test_generated_list_keeps_legacy_default_size(ers_client):
    responses.add(responses.GET, BASE, json={"SearchResult": {"total": 0}}, status=200)
    ers_client.get_endpoints()
    assert responses.calls[-1].request.url.endswith("size=20&page=1") or "size=20" in responses.calls[-1].request.url


@responses.activate
@pytest.mark.parametrize(
    "total, expected_pages", [(0, 1), (1, 1), (100, 1), (101, 2), (200, 2)]
)
def test_get_all_endpoint_groups_requests_ceiling_pages(
    ers_client, total, expected_pages
):
    responses.add(
        responses.GET,
        GROUP_BASE,
        json={"SearchResult": {"total": total, "resources": []}},
        status=200,
    )
    with aioresponses() as mocked:
        for page in range(1, 4):
            mocked.get(
                f"{GROUP_BASE}?page={page}&size=100",
                payload={"SearchResult": {"total": total, "resources": []}},
                repeat=True,
            )
        ers_client.get_all_endpoint_groups()

        pages = [
            int(url.query["page"])
            for (method, url) in mocked.requests
            if method == "GET" and url.query.get("size") == "100"
        ]

    assert sorted(pages) == list(range(1, expected_pages + 1))


def test_generate_check_rejects_stale_output(tmp_path, monkeypatch):
    output = tmp_path / "ers_read.py"
    output.write_text("# stale\n")
    monkeypatch.setattr(generate_module, "OUTPUT", output)

    assert generate_module.main(["--check"]) == 1
    assert generate_module.main([]) == 0
    assert generate_module.main(["--check"]) == 0
    assert "class ERSGeneratedMethods" in output.read_text()


def test_generated_methods_match_manifest_and_oid_guard_count():
    specs = load_specs(MANIFEST)
    tree = ast.parse(render(specs))
    cls = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "ERSGeneratedMethods"
    )
    funcs = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
    names = [node.name for node in funcs]
    expected = [method for spec in specs for method in spec.methods.values()]

    assert set(names) == set(expected)
    assert len(names) == len(expected)
    guard_count = sum(
        any(
            isinstance(node, ast.Attribute) and node.attr == "_oid_test"
            for node in ast.walk(func)
        )
        for func in funcs
    )
    assert guard_count == sum(spec.validate_oid for spec in specs)


def test_render_rejects_unknown_operation():
    specs = load_specs(MANIFEST)
    bad = replace(specs[0], methods={**specs[0].methods, "typo": "get_typo"})

    with pytest.raises(ValueError, match="unknown operation 'typo'"):
        render([bad])


def test_render_rejects_duplicate_method_names():
    specs = load_specs(MANIFEST)
    duplicate = replace(specs[0], name="duplicate_spec")

    with pytest.raises(ValueError, match="duplicate generated method name"):
        render([duplicate, *specs])


def test_render_rejects_unknown_list_signature():
    specs = load_specs(MANIFEST)
    bad = replace(specs[0], list_signature="bogus")

    with pytest.raises(ValueError, match="unknown list_signature 'bogus'"):
        render([bad])


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get_guestSmtpNotificationSettings", "config/guestsmtpnotificationsettings"),
        ("get_sxpLocalBindings", "config/sxplocalbindings"),
        ("get_tacacsCommandSets", "config/tacacscommandsets"),
        ("get_tacacsExternalServers", "config/tacacsexternalservers"),
    ],
)
def test_corrected_paths_are_used_by_generated_lists(ers_client, monkeypatch, method, path):
    captured = {}

    def capture(url, **kwargs):
        captured["url"] = url
        return {"success": True, "response": [], "error": ""}

    monkeypatch.setattr(ers_client, "_get_objects", capture)
    getattr(ers_client, method)()
    assert captured["url"].endswith(f"/{path}")


@responses.activate
@pytest.mark.parametrize(
    ("method", "path", "fixture", "wrapper"),
    [
        (
            "get_guestSmtpNotificationSetting_id",
            "config/guestsmtpnotificationsettings",
            "ers/guestSmtpNotificationSetting_by_id.json",
            "ERSGuestSmtpNotificationSettings",
        ),
        (
            "get_tacacsCommandSet_id",
            "config/tacacscommandsets",
            "ers/tacacsCommandSet_by_id.json",
            "TacacsCommandSets",
        ),
    ],
)
def test_corrected_by_id_paths_parse_live_key_fixtures(
    ers_client, method, path, fixture, wrapper
):
    body = load_fixture(fixture)
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/{path}/{VALID_OID}",
        json=body,
        status=200,
    )
    assert getattr(ers_client, method)(VALID_OID)["response"] == body[wrapper]


@pytest.mark.parametrize(
    "method, path",
    [
        ("get_smsProviders", "config/smsprovider"),
        ("get_sponsorGroupMembers", "config/sponsorgroupmember"),
    ],
)
def test_size_first_lists_keep_positional_size(ers_client, monkeypatch, method, path):
    captured = {}

    def capture(url, **kwargs):
        captured.update(kwargs)
        captured["url"] = url
        return {"success": True, "response": [], "error": ""}

    monkeypatch.setattr(ers_client, "_get_objects", capture)
    getattr(ers_client, method)(50)

    assert captured["size"] == 50
    assert captured["filter"] is None
    assert captured["page"] == 1
    assert captured["url"].endswith(f"/{path}")


def test_filter_first_lists_keep_positional_filter(ers_client, monkeypatch):
    captured = {}

    def capture(url, **kwargs):
        captured.update(kwargs)
        captured["url"] = url
        return {"success": True, "response": [], "error": ""}

    monkeypatch.setattr(ers_client, "_get_objects", capture)
    ers_client.get_endpoints("name.EQ.foo")

    assert captured["filter"] == "name.EQ.foo"
    assert captured["size"] == 20
    assert captured["page"] == 1


def test_generated_list_signatures_preserve_positional_semantics():
    size_first = inspect.signature(ERS.get_smsProviders)
    assert list(size_first.parameters) == ["self", "size", "page", "filter"]
    assert size_first.parameters["size"].default == 20
    assert size_first.parameters["page"].default == 1
    assert size_first.parameters["filter"].kind is inspect.Parameter.KEYWORD_ONLY

    filter_first = inspect.signature(ERS.get_endpoints)
    assert list(filter_first.parameters) == ["self", "filter", "size", "page"]
    assert filter_first.parameters["size"].default == 20


@responses.activate
@pytest.mark.parametrize(
    ("method", "path", "fixture", "wrapper"),
    [
        ("get_ancPolicy_id", "config/ancpolicy", "ers/ancPolicy_by_id.json", "ANCPolicy"),
        ("get_node_id", "config/node", "ers/node_by_id.json", "Node"),
        (
            "get_sessionServiceNode_id",
            "config/sessionservicenode",
            "ers/sessionServiceNode_by_id.json",
            "SessionServiceNode",
        ),
    ],
)
def test_new_core_by_id_reads_parse_live_key_fixtures(
    ers_client, method, path, fixture, wrapper
):
    body = load_fixture(fixture)
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/{path}/{VALID_OID}",
        json=body,
        status=200,
    )
    assert getattr(ers_client, method)(VALID_OID)["response"] == body[wrapper]


@responses.activate
def test_pxGridNode_list_parses_empty_live_fixture(ers_client):
    body = load_fixture("ers/pxGridNode_list.json")
    responses.add(
        responses.GET,
        "https://ise.test.invalid:9060/ers/config/pxgridnode",
        json=body,
        status=200,
    )
    result = ers_client.get_pxGridNodes()
    assert result["response"] == []
    assert result["success"] is True


@pytest.mark.parametrize(
    ("method_name", "expected_wrapper"),
    [
        ("get_ancPolicy_id", "ANCPolicy"),
        ("get_node_id", "Node"),
        ("get_sessionServiceNode_id", "SessionServiceNode"),
        ("get_pxGridNode_id", "PxgridNode"),
    ],
)
def test_new_core_by_key_uses_manifest_wrapper(
    ers_client, monkeypatch, method_name, expected_wrapper
):
    captured = []

    def capture_wrapper(url, objectid, objecttype):
        captured.append(objecttype)
        return {"success": True, "response": {}, "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", capture_wrapper)
    getattr(ers_client, method_name)(VALID_OID)

    assert captured == [expected_wrapper]


@responses.activate
def test_ancEndpoint_list_parses_empty_fixture(ers_client):
    body = load_fixture("ers/ancEndpoint_list.json")
    responses.add(
        responses.GET,
        "https://ise.test.invalid:9060/ers/config/ancendpoint",
        json=body,
        status=200,
    )
    result = ers_client.get_ancEndpoints()
    assert result["response"] == []
    assert result["success"] is True


@responses.activate
def test_service_list_parses_null_id_resource(ers_client):
    body = load_fixture("ers/service_list.json")
    responses.add(
        responses.GET,
        "https://ise.test.invalid:9060/ers/config/service",
        json=body,
        status=200,
    )
    result = ers_client.get_services()
    assert result["total"] == 1
    assert isinstance(result["response"], list)
    assert len(result["response"]) == 1
    assert isinstance(result["response"][0], dict)


@responses.activate
@pytest.mark.parametrize(
    ("method", "path", "fixture", "wrapper"),
    [
        (
            "get_telemetryInfo_id",
            "config/telemetryinfo",
            "ers/telemetryInfo_by_id.json",
            "TelemetryInfo",
        ),
        (
            "get_supportBundleStatus_id",
            "config/supportbundlestatus",
            "ers/supportBundleStatus_by_id.json",
            "SBStatus",
        ),
    ],
)
def test_partial_shape_by_id_reads_parse_live_key_fixtures(
    ers_client, method, path, fixture, wrapper
):
    body = load_fixture(fixture)
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/{path}/{VALID_OID}",
        json=body,
        status=200,
    )
    assert getattr(ers_client, method)(VALID_OID)["response"] == body[wrapper]


@pytest.mark.parametrize(
    ("method_name", "expected_wrapper"),
    [
        ("get_ancEndpoint_id", "ANCEndPoint"),
        ("get_service_id", "ERSService"),
        ("get_telemetryInfo_id", "TelemetryInfo"),
        ("get_supportBundleStatus_id", "SBStatus"),
    ],
)
def test_partial_shape_by_key_uses_manifest_wrapper(
    ers_client, monkeypatch, method_name, expected_wrapper
):
    captured = []

    def capture_wrapper(url, objectid, objecttype):
        captured.append(objecttype)
        return {"success": True, "response": {}, "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", capture_wrapper)
    getattr(ers_client, method_name)(VALID_OID)

    assert captured == [expected_wrapper]


@responses.activate
@pytest.mark.parametrize(
    ("method_name", "path", "fixture"),
    [
        ("get_threat_versionInfo", "config/threat", "ers/threat_versioninfo.json"),
        (
            "get_deploymentInfo_versionInfo",
            "config/deploymentinfo",
            "ers/deploymentInfo_versioninfo.json",
        ),
        (
            "get_restIdStoreAttribute_versionInfo",
            "config/restidstoreattribute",
            "ers/restIdStoreAttribute_versioninfo.json",
        ),
        (
            "get_restIdStoreSettings_versionInfo",
            "config/restidstoresettings",
            "ers/restIdStoreSettings_versioninfo.json",
        ),
        (
            "get_supportBundleDownload_versionInfo",
            "config/supportbundledownload",
            "ers/supportBundleDownload_versioninfo.json",
        ),
        (
            "get_supportBundle_versionInfo",
            "config/supportbundle",
            "ers/supportBundle_versioninfo.json",
        ),
    ],
)
def test_version_info_only_resources_parse_version_info_fixture(
    ers_client, method_name, path, fixture
):
    body = load_fixture(fixture)
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/{path}/versioninfo",
        json=body,
        status=200,
    )
    result = getattr(ers_client, method_name)()
    assert result["response"] == body["VersionInfo"]


@responses.activate
def test_version_info_only_resource_returns_405_result_contract(ers_client):
    responses.add(
        responses.GET,
        "https://ise.test.invalid:9060/ers/config/deploymentinfo/versioninfo",
        json={"ERSResponse": {"messages": [{"title": "Unsupported", "type": "ERROR"}]}},
        status=405,
    )
    result = ers_client.get_deploymentInfo_versionInfo()
    assert result["success"] is False
    assert result["error"] != ""


# (method, operation, path, lookup value, wrapper) for every method added by the
# ERS docs-coverage tasks. Pin the exact call shape so generator drift is caught.
NEW_GENERATED_READ_SHAPES = [
    # Keyword-only-filter lists.
    ("get_ancPolicies", "list", "config/ancpolicy", None, None),
    ("get_nodes", "list", "config/node", None, None),
    ("get_sessionServiceNodes", "list", "config/sessionservicenode", None, None),
    ("get_pxGridNodes", "list", "config/pxgridnode", None, None),
    ("get_ancEndpoints", "list", "config/ancendpoint", None, None),
    ("get_services", "list", "config/service", None, None),
    ("get_telemetryInfos", "list", "config/telemetryinfo", None, None),
    ("get_supportBundleStatuses", "list", "config/supportbundlestatus", None, None),
    # By-id reads.
    ("get_ancPolicy_id", "id", "config/ancpolicy", VALID_OID, "ANCPolicy"),
    ("get_node_id", "id", "config/node", VALID_OID, "Node"),
    (
        "get_sessionServiceNode_id",
        "id",
        "config/sessionservicenode",
        VALID_OID,
        "SessionServiceNode",
    ),
    ("get_pxGridNode_id", "id", "config/pxgridnode", VALID_OID, "PxgridNode"),
    ("get_ancEndpoint_id", "id", "config/ancendpoint", VALID_OID, "ANCEndPoint"),
    ("get_service_id", "id", "config/service", VALID_OID, "ERSService"),
    ("get_telemetryInfo_id", "id", "config/telemetryinfo", VALID_OID, "TelemetryInfo"),
    (
        "get_supportBundleStatus_id",
        "id",
        "config/supportbundlestatus",
        VALID_OID,
        "SBStatus",
    ),
    # By-name reads.
    ("get_ancPolicy_name", "name", "config/ancpolicy", "sample-name", "ANCPolicy"),
    ("get_node_name", "name", "config/node", "sample-name", "Node"),
    (
        "get_sessionServiceNode_name",
        "name",
        "config/sessionservicenode",
        "sample-name",
        "SessionServiceNode",
    ),
    ("get_pxGridNode_name", "name", "config/pxgridnode", "sample-name", "PxgridNode"),
    # VersionInfo reads.
    ("get_ancPolicy_versionInfo", "versioninfo", "config/ancpolicy", "", "VersionInfo"),
    ("get_node_versionInfo", "versioninfo", "config/node", "", "VersionInfo"),
    (
        "get_sessionServiceNode_versionInfo",
        "versioninfo",
        "config/sessionservicenode",
        "",
        "VersionInfo",
    ),
    ("get_pxGridNode_versionInfo", "versioninfo", "config/pxgridnode", "", "VersionInfo"),
    ("get_ancEndpoint_versionInfo", "versioninfo", "config/ancendpoint", "", "VersionInfo"),
    ("get_service_versionInfo", "versioninfo", "config/service", "", "VersionInfo"),
    (
        "get_telemetryInfo_versionInfo",
        "versioninfo",
        "config/telemetryinfo",
        "",
        "VersionInfo",
    ),
    (
        "get_supportBundleStatus_versionInfo",
        "versioninfo",
        "config/supportbundlestatus",
        "",
        "VersionInfo",
    ),
    ("get_threat_versionInfo", "versioninfo", "config/threat", "", "VersionInfo"),
    ("get_deploymentInfo_versionInfo", "versioninfo", "config/deploymentinfo", "", "VersionInfo"),
    (
        "get_restIdStoreAttribute_versionInfo",
        "versioninfo",
        "config/restidstoreattribute",
        "",
        "VersionInfo",
    ),
    (
        "get_restIdStoreSettings_versionInfo",
        "versioninfo",
        "config/restidstoresettings",
        "",
        "VersionInfo",
    ),
    (
        "get_supportBundleDownload_versionInfo",
        "versioninfo",
        "config/supportbundledownload",
        "",
        "VersionInfo",
    ),
    ("get_supportBundle_versionInfo", "versioninfo", "config/supportbundle", "", "VersionInfo"),
]


@pytest.mark.parametrize(
    ("method", "operation", "path", "lookup", "wrapper"),
    NEW_GENERATED_READ_SHAPES,
)
def test_new_generated_read_shapes_are_pinned(
    ers_client, monkeypatch, method, operation, path, lookup, wrapper
):
    captured = {}

    def capture_object(url, objectid, objecttype):
        captured.update(url=url, objectid=objectid, objecttype=objecttype)
        return {"success": True, "response": {}, "error": ""}

    def capture_objects(url, *, filter, size, page):
        captured.update(url=url, filter=filter, size=size, page=page)
        return {"success": True, "response": [], "error": ""}

    monkeypatch.setattr(ers_client, "_get_object", capture_object)
    monkeypatch.setattr(ers_client, "_get_objects", capture_objects)

    args = () if operation in ("list", "versioninfo") else (lookup,)
    getattr(ers_client, method)(*args)

    suffix = {"id": "", "name": "/name", "versioninfo": "/versioninfo"}.get(operation, "")
    assert captured["url"] == f"{ers_client.url_base}/{path}{suffix}"
    if operation == "list":
        assert captured["filter"] is None
        assert captured["size"] == 20
        assert captured["page"] == 1
    else:
        assert captured["objectid"] == lookup
        assert captured["objecttype"] == wrapper


@pytest.mark.parametrize(
    "method", [row[0] for row in NEW_GENERATED_READ_SHAPES if row[1] == "list"]
)
def test_new_generated_lists_keep_keyword_only_filter(method):
    signature = inspect.signature(getattr(ERS, method))
    assert list(signature.parameters) == ["self", "size", "page", "filter"]
    assert signature.parameters["size"].default == 20
    assert signature.parameters["page"].default == 1
    assert signature.parameters["filter"].default is None
    assert signature.parameters["filter"].kind is inspect.Parameter.KEYWORD_ONLY
