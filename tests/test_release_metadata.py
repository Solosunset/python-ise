from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_license_is_gplv2() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in text
    assert "Version 2, June 1991" in text
    assert "MIT License" not in text


def test_package_metadata_matches_license() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]
    assert project["license"]["file"] == "LICENSE"
    assert "License :: OSI Approved :: GNU General Public License v2 (GPLv2)" in project["classifiers"]
    assert "OpenAPI" not in project["description"]
    assert "mnt" in project["keywords"]


def test_package_metadata_does_not_claim_openapi() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "openapi" not in str(data["project"]).lower()


def test_readme_documents_gplv2_and_provenance() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "GPLv2" in text
    assert "NOTICE.md" in text
    assert "falkowich/ise" in text
    assert "MIT — see" not in text


def test_notice_credits_upstream() -> None:
    text = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    assert "falkowich/ise" in text
    assert "GPL-2.0-only" in text
