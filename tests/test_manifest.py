from pathlib import Path

import pytest

from scripts.audit_endpoints import audit_public_methods
from python_ise.spec import EndpointSpec, load_specs

ROOT = Path(__file__).resolve().parents[1]
ERS_MANIFEST = ROOT / "src/python_ise/manifest/ers.yaml"
ERS_MODULE = ROOT / "src/python_ise/python_ise.py"

def test_audit_detects_no_shadowed_public_names():
    duplicates = audit_public_methods(ERS_MODULE)
    assert duplicates == {}

def test_manifest_seeds_known_resources():
    specs = {s.name: s for s in load_specs(ERS_MANIFEST)}
    assert specs["endpoint"].wrapper == "ERSEndPoint"
    assert specs["identityGroup"].wrapper == "IdentityGroup"
    assert specs["endpoint"].methods["by_id"] == "get_endpoint_id"
    assert specs["endpoint"].special is False


@pytest.mark.parametrize(
    ("name", "field", "expected"),
    [
        ("guestSmtpNotificationSetting", "path", "config/guestsmtpnotificationsettings"),
        ("sxpLocalBinding", "path", "config/sxplocalbindings"),
        ("tacacsCommandSet", "path", "config/tacacscommandsets"),
        ("tacacsExternalServer", "path", "config/tacacsexternalservers"),
        ("guestSmtpNotificationSetting", "wrapper", "ERSGuestSmtpNotificationSettings"),
        ("tacacsCommandSet", "wrapper", "TacacsCommandSets"),
    ],
)
def test_manifest_paths_and_wrappers_match_live_sdk(name, field, expected):
    specs = {s.name: s for s in load_specs(ERS_MANIFEST)}
    assert getattr(specs[name], field) == expected
