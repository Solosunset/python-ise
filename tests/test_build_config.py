from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_build_config_has_no_force_include() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    hatch = data["tool"]["hatch"]["build"]

    assert "force-include" not in hatch
    assert hatch["targets"]["wheel"]["packages"] == ["src/python_ise"]

    include = hatch["targets"]["sdist"]["include"]
    for item in ("src/python_ise", "README.md", "LICENSE", "NOTICE.md"):
        assert item in include
