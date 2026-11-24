"""Guard the manifest against regressions in verified ERS SDK resource coverage."""

from pathlib import Path

from python_ise.spec import load_specs

MANIFEST = Path(__file__).resolve().parents[1] / "src/python_ise/manifest/ers.yaml"

# Resource IDs copied from /ers/sdk with namespace prefixes stripped. Sanitized:
# no hostnames or credentials.
SDK_RESOURCE_TAILS = {
    "ancendpoint", "ancpolicy", "acibindings", "acisettings", "activedirectory",
    "adminuser", "portalglobalsetting", "allowedprotocols", "authorizationprofile",
    "byodportal", "certificatetemplate", "certificateprofile", "threat",
    "downloadableacl", "egressmatrixcell", "endpoint", "endpointcert",
    "endpointgroup", "externalradiusserver", "filterpolicy", "guestlocation",
    "guestsmtpnotificationsettings", "guestssid", "guesttype", "guestuser",
    "hotspotportal", "sgmapping", "sgmappinggroup", "service", "identitygroup",
    "idstoresequence", "internaluser", "mydeviceportal", "nspprofile",
    "networkdevice", "networkdevicegroup", "node", "sessionservicenode",
    "portal", "portaltheme", "profilerprofile", "deploymentinfo", "pxgridnode",
    "pxgridsettings", "radiusserversequence", "restidstore",
    "restidstoreattribute", "restidstoresettings", "smsprovider",
    "sxpconnections", "sxplocalbindings", "sxpvpns", "sgt", "sgacl",
    "sgtvnvlan", "selfregportal", "sponsorgroup", "sponsorgroupmember",
    "sponsorportal", "sponsoredguestportal", "supportbundledownload",
    "supportbundlestatus", "supportbundle", "systemcertificate",
    "tacacscommandsets", "tacacsexternalservers", "tacacsprofile",
    "tacacsserversequence", "telemetryinfo",
}


def test_every_sdk_resource_is_in_manifest():
    tails = {spec.path.removeprefix("config/") for spec in load_specs(MANIFEST)}
    assert SDK_RESOURCE_TAILS - tails == set()


def test_ldap_is_documented_as_an_unverified_legacy_resource():
    spec = {s.name: s for s in load_specs(MANIFEST)}["ldap"]
    assert spec.path == "config/ldap"
    assert "500" in spec.notes
    assert "not in SDK" in spec.notes
