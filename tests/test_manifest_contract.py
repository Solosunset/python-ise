import ast
from pathlib import Path
import pytest
from scripts.audit_endpoints import audit_public_methods
from python_ise.generate import render
from python_ise.spec import load_specs

ERS_MANIFEST = Path("src/python_ise/manifest/ers.yaml")
GENERATED = Path("src/python_ise/generated/ers_read.py")

def test_no_duplicate_public_methods_in_ers_class():
    assert audit_public_methods(Path("src/python_ise/python_ise.py")) == {}  # RF-1

def test_no_stale_hand_written_copy_of_generated_method():
    generated_names = {line.split("def ", 1)[1].split("(", 1)[0]
                       for line in GENERATED.read_text().splitlines() if line.strip().startswith("def ")}
    tree = ast.parse(Path("src/python_ise/python_ise.py").read_text(encoding="utf-8"))
    hand_written = {
        item.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        for item in node.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_")
    }
    assert hand_written & generated_names == set()  # a direct definition would shadow the generated mixin

def test_generated_file_is_current():
    assert render(load_specs(ERS_MANIFEST)) == GENERATED.read_text()

def test_seed_resources_have_fixtures():
    prefixes = {p.name.split("_", 1)[0] for p in Path("tests/fixtures/ers").glob("*.json")}
    specs = load_specs(ERS_MANIFEST)
    seeded = {s.name for s in specs if s.name in {"endpoint", "identityGroup", "sgt"}}
    assert seeded <= prefixes

def test_every_generated_method_comes_from_manifest():
    generated = GENERATED.read_text()
    for spec in load_specs(ERS_MANIFEST):
        for method_name in spec.methods.values():
            assert f"def {method_name}(" in generated

def test_every_wrapper_key_cites_a_source():
    for spec in load_specs(ERS_MANIFEST):
        assert spec.wrapper in spec.notes or "developer.cisco.com" in spec.notes, spec.name

def test_stale_copy_guard_detects_injected_generated_method(monkeypatch):
    stale_name = "get_endpoint_id"
    assert f"def {stale_name}(" in GENERATED.read_text()
    injected_source = f"class Legacy:\n    def {stale_name}(self, OID):\n        return {{}}\n"
    real_read_text = Path.read_text

    def read_text(path, *args, **kwargs):
        if path.name == "python_ise.py":
            return injected_source
        return real_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    with pytest.raises(AssertionError, match=stale_name):
        test_no_stale_hand_written_copy_of_generated_method()
