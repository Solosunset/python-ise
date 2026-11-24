from pathlib import Path

import responses

from python_ise import ERS
from python_ise.spec import load_specs
from tests.helpers import load_fixture

# The fixture body id is 8-4-4-12; _oid_test accepts only 8-4-4-4-12 for requests.
OID = "abcd1234-ef56-7890-abcd1234ef56"
VALID_OID = "abcd1234-ef56-7890-abcd-1234ef56abcd"
ERS_MANIFEST = Path("src/python_ise/manifest/ers.yaml")


@responses.activate
def test_legacy_flat_method_still_works(ers_client):
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/config/endpoint/{VALID_OID}",
        json=load_fixture("ers/endpoint_by_id.json"),
        status=200,
    )
    assert ers_client.get_endpoint_id(VALID_OID)["response"]["id"] == OID


@responses.activate
def test_namespace_facade_delegates(ers_client):
    from python_ise.client import ISEClient
    responses.add(
        responses.GET,
        f"https://ise.test.invalid:9060/ers/config/endpoint/{VALID_OID}",
        json=load_fixture("ers/endpoint_by_id.json"),
        status=200,
    )
    assert ISEClient(ers=ers_client).endpoints.get(VALID_OID)["response"]["id"] == OID


def test_every_legacy_name_still_resolves():
    from python_ise.generated.aliases import LEGACY_NAMES

    for spec_name, names in LEGACY_NAMES.items():
        for name in names:
            assert callable(getattr(ERS, name)), f"{spec_name}: {name}"


def test_generated_aliases_match_manifest():
    from python_ise.generated.aliases import FACADE_SPECS, LEGACY_NAMES

    specs = load_specs(ERS_MANIFEST)
    assert LEGACY_NAMES == {spec.name: tuple(spec.legacy_names) for spec in specs}
    assert tuple((plural, dict(methods)) for plural, methods in FACADE_SPECS) == tuple(
        (spec.plural, dict(spec.methods)) for spec in specs
    )


def test_generate_check_rejects_stale_aliases(tmp_path, monkeypatch):
    from python_ise import generate

    ers_output = tmp_path / "ers_read.py"
    aliases_output = tmp_path / "aliases.py"
    ers_output.write_text(generate.render(load_specs(ERS_MANIFEST)), encoding="utf-8")
    aliases_output.write_text("# deliberately stale\n", encoding="utf-8")
    monkeypatch.setattr(generate, "OUTPUT", ers_output)
    monkeypatch.setattr(generate, "ALIASES_OUTPUT", aliases_output)

    assert generate.main(["--check"]) == 1
    assert generate.main([]) == 0
    assert generate.main(["--check"]) == 0
    assert "FACADE_SPECS" in aliases_output.read_text(encoding="utf-8")
