from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_publish_workflow_is_manual_and_confirmed() -> None:
    data = yaml.safe_load(
        (ROOT / ".github" / "workflows" / "publish.yml").read_text(encoding="utf-8")
    )
    triggers = data["on"]

    assert "workflow_dispatch" in triggers
    assert "push" not in triggers

    inputs = triggers["workflow_dispatch"]["inputs"]
    assert inputs["target"]["type"] == "choice"
    assert inputs["target"]["choices"] == ["testpypi", "pypi"]
    assert inputs["target"]["default"] == "testpypi"
    assert inputs["confirm"]["default"] == "false"

    jobs = data["jobs"]
    assert "build" in jobs
    assert jobs["publish-testpypi"]["needs"] == "build"
    assert jobs["publish-pypi"]["needs"] == "build"
    assert jobs["publish-testpypi"]["environment"] == "testpypi"
    assert jobs["publish-pypi"]["environment"] == "pypi"
    assert "inputs.target == 'testpypi'" in jobs["publish-testpypi"]["if"]
    assert "inputs.target == 'pypi'" in jobs["publish-pypi"]["if"]
    assert "inputs.confirm == 'true'" in jobs["publish-testpypi"]["if"]
    assert "inputs.confirm == 'true'" in jobs["publish-pypi"]["if"]
