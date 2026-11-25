# GPLv2 Public Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public `python-ise` package legally accurate, buildable as both sdist and wheel, and ready for separately approved TestPyPI and PyPI releases under GPLv2.

**Architecture:** First align license, metadata, and provenance with the upstream GPLv2 source. Then add source notices without hand-editing generated modules, repair the Hatch build configuration, and add a manual-only publish workflow. Release execution remains approval-gated and is not part of the approved implementation scope.

**Tech Stack:** Python `>=3.12`, `uv`, Hatchling, pytest, PyYAML, GitHub Actions, PyPI Trusted Publishing (OIDC).

**Spec:** `docs/plans/2026-11-25-public-release-design.md`

## Global Constraints

- Python `>=3.12`; `uv` is the project tool.
- Offline gates must stay green: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.
- Generated files under `src/python_ise/generated/` are never hand-edited.
- Commit identity for new commits: `SoloSunset <mathias@mdkp.dk>`.
- Public repo canonical SSH remote: `git@github.com:Solosunset/python-ise.git`.
- Plan documents live in `docs/plans/`; `docs/superpowers/` stays out of the published tree.
- Upstream is `GPL-2.0-only` for this plan.
- Commercial use is allowed; GPLv2 source, notice, and licensing obligations apply to redistribution.
- No publish to TestPyPI or PyPI without separate explicit user approval.
- No push, PR, tag, remote, or GitHub setting change without explicit user approval.
- No real passwords, IPs, hostnames, internal URLs, ticket IDs, or colleague names in published files or commit messages.
- TestPyPI already has `python-ise 0.1.4`; real PyPI does not have the name.
- Release versions: `0.2.0rc1` on TestPyPI, `0.2.0` on PyPI.
- OpenAPI is not implemented and must not be advertised in `0.2.0`.

## Review Focus

- A leftover MIT license or classifier would misstate rights. Pinned by `tests/test_release_metadata.py::test_license_is_gplv2` and `test_package_metadata_matches_license` in Task 1.
- Package metadata claiming OpenAPI would advertise a feature that does not exist. Pinned by `test_package_metadata_does_not_claim_openapi` in Task 1.
- Generated modules could lose notices on the next regeneration. Pinned by `tests/test_release_metadata.py::test_generated_files_carry_gpl_notice` in Task 2, after regeneration from templates.
- A source distribution that omits manifest/templates breaks wheel builds from the sdist. Pinned by `tests/test_build_config.py::test_build_config_has_no_force_include` in Task 3 plus the `uv build` artifact inspection in Task 5.
- A release workflow with a push trigger or without confirmation could publish accidentally. Pinned by `tests/test_publish_workflow.py::test_publish_workflow_is_manual_and_confirmed` in Task 4.

---

### Task 1: License and provenance metadata

**Files:**
- Modify: `LICENSE`
- Create: `NOTICE.md`
- Modify: `README.md`
- Modify: `pyproject.toml`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: none.
- Produces: `LICENSE` containing GPLv2 text; `NOTICE.md` with upstream attribution; project metadata with `GPL-2.0-only` classifier and corrected description.

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_release_metadata.py -q`
Expected: FAIL because MIT license, MIT classifier, stale description, and missing `NOTICE.md` are still present.

- [ ] **Step 3: Replace the license text**

In `LICENSE`, replace the MIT text verbatim with the GNU General Public License version 2 text from `https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt`. Do not add "or later" language.

- [ ] **Step 4: Add provenance notice**

Create `NOTICE.md` with these facts:
- Project: `python-ise`.
- License: `GPL-2.0-only`.
- Derived from `falkowich/ise` at `https://github.com/falkowich/ise`.
- Earlier contributors credited by that project: `bobthebutcher`, `mpenning`, `karrots`, `msom`.
- Statement that this project is not affiliated with Cisco or the upstream authors.
- Statement that GPLv2 permits commercial use and redistribution subject to its terms.

- [ ] **Step 5: Update README**

In `README.md`, change the License section to say `GPLv2 — see LICENSE and NOTICE.md` and change the Credits section to name `falkowich/ise` as the upstream source and link `NOTICE.md`. Keep the existing "No OpenAPI support yet" status line.

- [ ] **Step 6: Update package metadata**

In `pyproject.toml`:
- Keep `license = { file = "LICENSE" }`.
- Replace the MIT classifier with `License :: OSI Approved :: GNU General Public License v2 (GPLv2)`.
- Change `description` to `Library to interact with Cisco ISE's ERS and MNT APIs`.
- Keep `keywords = ["cisco", "ise", "ers", "mnt", "sdk"]`.

- [ ] **Step 7: Run tests and offline gates**

Run: `uv run pytest tests/test_release_metadata.py -q`
Expected: PASS.

Run: `uv run pytest -q`
Expected: PASS with 142 existing tests plus the new tests.

Run: `uv run python -m python_ise.generate --check`
Expected: no output, exit 0.

- [ ] **Step 8: Commit**

```bash
git add LICENSE NOTICE.md README.md pyproject.toml tests/test_release_metadata.py
git commit -m "docs: switch package to GPLv2 provenance"
```

### Task 2: Source-file GPL notices

**Files:**
- Modify: `src/python_ise/__init__.py`
- Modify: `src/python_ise/client.py`
- Modify: `src/python_ise/generate.py`
- Modify: `src/python_ise/python_ise.py`
- Modify: `src/python_ise/spec.py`
- Modify: `src/python_ise/templates/ers_read.py.j2`
- Modify: `src/python_ise/templates/aliases.py.j2`
- Regenerate: `src/python_ise/generated/ers_read.py`
- Regenerate: `src/python_ise/generated/aliases.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: the GPLv2 license and attribution text from Task 1.
- Produces: every hand-maintained source file and generated module carries the same GPLv2 notice.

- [ ] **Step 1: Add failing notice tests**

Append to `tests/test_release_metadata.py`:

```python
SOURCE_FILES = (
    "src/python_ise/__init__.py",
    "src/python_ise/client.py",
    "src/python_ise/generate.py",
    "src/python_ise/python_ise.py",
    "src/python_ise/spec.py",
    "src/python_ise/templates/ers_read.py.j2",
    "src/python_ise/templates/aliases.py.j2",
)
GENERATED_FILES = (
    "src/python_ise/generated/ers_read.py",
    "src/python_ise/generated/aliases.py",
)


def test_source_files_carry_gpl_notice() -> None:
    for relative_path in SOURCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert "GNU General Public License" in text, relative_path
        assert "falkowich/ise" in text, relative_path


def test_generated_files_carry_gpl_notice() -> None:
    for relative_path in GENERATED_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert "GNU General Public License" in text, relative_path
        assert "falkowich/ise" in text, relative_path
```

Do not assert on `src/python_ise/generated/__init__.py`; it is not produced by the generator and is covered by package-level notices.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_release_metadata.py -q -k notice`
Expected: FAIL for both tests.

- [ ] **Step 3: Add the notice to hand-maintained files**

Add this comment block at the top of each file in `SOURCE_FILES`, after any existing module docstring:

```python
# Copyright (C) 2026 SoloSunset
# Derived from falkowich/ise.
#
# This file is part of python-ise and is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License,
# version 2 only, as published by the Free Software Foundation.
#
# python-ise is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with python-ise. If not, see <https://www.gnu.org/licenses/>.
```

Use the same `#` comment syntax in the `.j2` templates. Keep existing code and docstrings unchanged apart from the inserted notice.

- [ ] **Step 4: Regenerate generated modules**

Run: `uv run python -m python_ise.generate`
Expected: `ers_read.py` and `aliases.py` are updated from the templates. Do not edit either file directly.

- [ ] **Step 5: Run tests and offline gates**

Run: `uv run pytest tests/test_release_metadata.py -q -k notice`
Expected: PASS.

Run: `uv run pytest -q`
Expected: PASS including all existing tests.

Run: `uv run python -m python_ise.generate --check`
Expected: no output, exit 0.

- [ ] **Step 6: Commit**

```bash
git add src/python_ise tests/test_release_metadata.py
git commit -m "docs: add GPLv2 source notices"
```

### Task 3: Repair Hatch sdist and wheel build

**Files:**
- Modify: `pyproject.toml`
- Test: `tests/test_build_config.py`

**Interfaces:**
- Consumes: `NOTICE.md` from Task 1.
- Produces: `uv build` produces sdist and wheel; wheel contains manifest and templates; wheel builds successfully from the sdist.

- [ ] **Step 1: Write the failing build-config test**

Create `tests/test_build_config.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_build_config.py -q`
Expected: FAIL because `force-include` is still present and no sdist include list exists.

- [ ] **Step 3: Replace the Hatch build configuration**

In `pyproject.toml`, replace the existing `[tool.hatch.build.targets.wheel]` and `[tool.hatch.build.force-include]` blocks with:

```toml
[tool.hatch.build.targets.sdist]
include = [
    "src/python_ise",
    "README.md",
    "LICENSE",
    "NOTICE.md",
]

[tool.hatch.build.targets.wheel]
packages = ["src/python_ise"]
```

Remove the entire `[tool.hatch.build.force-include]` section. Do not add a replacement force-include section.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_build_config.py -q`
Expected: PASS.

- [ ] **Step 5: Run offline gates**

Run: `uv run pytest -q`
Expected: PASS.

Run: `uv run python -m python_ise.generate --check`
Expected: no output, exit 0.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml tests/test_build_config.py
git commit -m "fix: build sdist and wheel without force-include"
```

### Task 4: Manual publish workflow and release docs

**Files:**
- Create: `.github/workflows/publish.yml`
- Create: `docs/releases.md`
- Modify: `CONTRIBUTING.md`
- Test: `tests/test_publish_workflow.py`

**Interfaces:**
- Consumes: build artifacts from `uv build`; Trusted Publishing configured outside the repository.
- Produces: a workflow that publishes only on manual dispatch with explicit confirmation.

- [ ] **Step 1: Write the failing workflow test**

Create `tests/test_publish_workflow.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_publish_workflow.py -q`
Expected: FAIL because `publish.yml` does not exist.

- [ ] **Step 3: Create the workflow**

Create `.github/workflows/publish.yml` with:
- `name: publish`.
- A quoted `"on":` key containing only `workflow_dispatch`.
- Inputs: `target` as a required choice with defaults and choices exactly as asserted; `confirm` as a required string with default `"false"`.
- Top-level `permissions: contents: read`.
- One job named `build` on `ubuntu-latest` that:
  - checks out with `actions/checkout@v4`;
  - installs `uv` with `astral-sh/setup-uv@v5`;
  - runs `uv sync --dev`;
  - runs `uv run pytest -q`;
  - runs `uv run python -m python_ise.generate --check`;
  - runs `uv build`;
  - runs `uvx twine check dist/*`;
  - uploads `dist/` with `actions/upload-artifact@v4`, artifact name `dist`.
- One job named `publish-testpypi` that:
  - has `needs: build`;
  - has `if` requiring `inputs.target == 'testpypi' && inputs.confirm == 'true'`;
  - uses `environment: testpypi`;
  - sets `permissions: id-token: write`;
  - downloads the `dist` artifact with `actions/download-artifact@v4` into `dist/`;
  - publishes with `pypa/gh-action-pypi-publish@release/v1`, `repository-url: https://test.pypi.org/legacy/`, `packages-dir: dist/`.
- One job named `publish-pypi` that:
  - has `needs: build`;
  - has `if` requiring `inputs.target == 'pypi' && inputs.confirm == 'true'`;
  - uses `environment: pypi`;
  - sets `permissions: id-token: write`;
  - downloads the `dist` artifact into `dist/`;
  - publishes with `pypa/gh-action-pypi-publish@release/v1`, `packages-dir: dist/`, and no custom repository URL.
- No hardcoded token, password, or API key anywhere in the file.

- [ ] **Step 4: Create release documentation**

Create `docs/releases.md` with:
- Statement that publishing always requires explicit user approval.
- Trusted Publisher prerequisites for both `testpypi` and `pypi`: owner `Solosunset`, repository `python-ise`, workflow `publish.yml`, matching environment name.
- TestPyPI procedure: bump to `0.2.0rc1`, run offline gates, commit, dispatch with `target=testpypi` and `confirm=true`, then install from TestPyPI and verify import.
- PyPI procedure: only after TestPyPI verification and a separate approval, bump to `0.2.0`, commit, dispatch with `target=pypi` and `confirm=true`.
- Statement that no tags trigger publishing.

- [ ] **Step 5: Link release docs from CONTRIBUTING**

Add one line under the contributing section or workflow heading in `CONTRIBUTING.md` linking to `docs/releases.md`.

- [ ] **Step 6: Run tests and offline gates**

Run: `uv run pytest tests/test_publish_workflow.py -q`
Expected: PASS.

Run: `uv run pytest -q`
Expected: PASS.

Run: `uv run python -m python_ise.generate --check`
Expected: no output, exit 0.

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"`
Expected: no output, exit 0.

- [ ] **Step 7: Commit**

```bash
git add .github/workflows/publish.yml docs/releases.md CONTRIBUTING.md tests/test_publish_workflow.py
git commit -m "ci: add manual GPLv2 release workflow"
```

### Task 5: Final offline verification and artifact audit

**Files:**
- No source changes expected.
- Create: `dist/` artifacts locally only; do not commit `dist/`.

**Interfaces:**
- Consumes: all changes from Tasks 1–4.
- Produces: evidence that sdist, wheel, tests, generation check, metadata, and leak checks are ready for approval.

- [ ] **Step 1: Run full offline gates**

Run: `uv run pytest -q`
Expected: PASS.

Run: `uv run python -m python_ise.generate --check`
Expected: no output, exit 0.

Run: `git diff --check`
Expected: no output, exit 0.

- [ ] **Step 2: Build and check artifacts**

Run: `uv build`
Expected: builds `dist/python_ise-0.2.0.tar.gz` only after the version is bumped in an approval-gated task. At this stage the current version is still `0.1.4`, so expected artifacts are `dist/python_ise-0.1.4.tar.gz` and `dist/python_ise-0.1.4-py3-none-any.whl`.

Run: `uvx twine check dist/*`
Expected: PASSED for both artifacts.

- [ ] **Step 3: Inspect artifact contents**

Run the following and confirm the listed files are present:

```bash
python - <<'PY'
import tarfile
import zipfile
from pathlib import Path

sdist = next(Path("dist").glob("*.tar.gz"))
wheel = next(Path("dist").glob("*.whl"))

with tarfile.open(sdist) as archive:
    sdist_names = archive.getnames()
with zipfile.ZipFile(wheel) as archive:
    wheel_names = archive.namelist()

for needle in ("LICENSE", "NOTICE.md", "manifest/ers.yaml", "templates/ers_read.py.j2"):
    assert any(needle in name for name in sdist_names), (needle, "sdist")
for needle in ("python_ise/manifest/ers.yaml", "python_ise/templates/ers_read.py.j2"):
    assert needle in wheel_names, (needle, "wheel")
print("sdist and wheel contents OK")
PY
```

Expected: `sdist and wheel contents OK`.

- [ ] **Step 4: Check for sensitive strings**

Run the existing focused scanner against the public clone and confirm no new high-signal findings beyond known synthetic fixtures:

```bash
REPO=. python /tmp/opencode/python-ise-audit/focused.py
```

Expected: no real credentials, real IPs, real hostnames, internal URLs, ticket IDs, or colleague names.

- [ ] **Step 5: Confirm clean working tree**

Run: `git status --short`
Expected: clean except untracked `dist/`, which is ignored or removed.

### Task 6: Approval-gated TestPyPI release

**Files:**
- Modify: `pyproject.toml` version only.

**Interfaces:**
- Consumes: all Task 1–5 changes and explicit user approval for TestPyPI.
- Produces: `python-ise 0.2.0rc1` on TestPyPI.

**Do not start this task without explicit user approval.**

- [ ] **Step 1: Confirm approval**

Record the user's explicit approval to publish to TestPyPI. If absent, stop.

- [ ] **Step 2: Bump version**

Set `version = "0.2.0rc1"` in `pyproject.toml`.

- [ ] **Step 3: Run offline gates**

Run: `uv run pytest -q`
Run: `uv run python -m python_ise.generate --check`
Run: `uv build`
Run: `uvx twine check dist/*`
Expected: all PASS.

- [ ] **Step 4: Commit and push only if separately approved**

If the user has approved a push, commit with message `chore: release 0.2.0rc1` and push the current branch. If not, stop before pushing.

- [ ] **Step 5: Dispatch TestPyPI publish**

After the user approves the specific dispatch, run the `publish` workflow manually with `target=testpypi` and `confirm=true`.

- [ ] **Step 6: Verify TestPyPI install**

In a clean virtual environment, install with:

```bash
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ python-ise==0.2.0rc1
python -c "import python_ise; print(python_ise.__all__)"
```

Expected: install succeeds and import prints the public API list.

### Task 7: Approval-gated PyPI release

**Files:**
- Modify: `pyproject.toml` version only.

**Interfaces:**
- Consumes: successful Task 6 verification and explicit user approval for PyPI.
- Produces: `python-ise 0.2.0` on PyPI.

**Do not start this task without explicit user approval and successful TestPyPI verification.**

- [ ] **Step 1: Confirm approval**

Record the user's explicit approval to publish to real PyPI. If absent, stop.

- [ ] **Step 2: Bump version**

Set `version = "0.2.0"` in `pyproject.toml`.

- [ ] **Step 3: Run offline gates**

Run: `uv run pytest -q`
Run: `uv run python -m python_ise.generate --check`
Run: `uv build`
Run: `uvx twine check dist/*`
Expected: all PASS.

- [ ] **Step 4: Commit and push only if separately approved**

If the user has approved a push, commit with message `chore: release 0.2.0` and push the current branch. If not, stop before pushing.

- [ ] **Step 5: Dispatch PyPI publish**

After the user approves the specific dispatch, run the `publish` workflow manually with `target=pypi` and `confirm=true`.

- [ ] **Step 6: Verify PyPI install**

In a clean virtual environment, install with:

```bash
uv pip install python-ise==0.2.0
python -c "import python_ise; print(python_ise.__all__)"
```

Expected: install succeeds and import prints the public API list.
