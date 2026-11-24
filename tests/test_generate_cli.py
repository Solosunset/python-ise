import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generate_check_succeeds_on_committed_tree():
    result = subprocess.run(
        [sys.executable, "-m", "python_ise.generate", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_generate_check_rejects_drifted_output(monkeypatch, tmp_path):
    from python_ise import generate

    stale = tmp_path / "ers_read.py"
    stale.write_text("# deliberately stale\n", encoding="utf-8")
    monkeypatch.setattr(generate, "OUTPUT", stale)
    assert generate.main(["--check"]) == 1


def test_ci_workflow_runs_generated_drift_check():
    text = (ROOT / ".github/workflows/generated-drift.yml").read_text(encoding="utf-8")
    assert "uv sync --dev" in text
    assert "python_ise.generate --check" in text
    assert "uv run pytest" in text


def test_agent_runbook_lists_required_steps():
    text = (ROOT / "docs/agent-runbook.md").read_text(encoding="utf-8")
    assert "docs/contracts/api-contract.md" in text
    assert "one agent session per endpoint" in text
