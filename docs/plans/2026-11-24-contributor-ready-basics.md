# Contributor-Ready Public Repo Basics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the public repository the minimum documentation and community guardrails needed to accept issues and contributions safely.

**Architecture:** Documentation-only changes on a dedicated branch of the public clone. No runtime code, manifest, fixture, generated module, or test behavior changes. Each task is independently verifiable and gets its own commit.

**Tech Stack:** Markdown, GitHub-flavored Markdown, YAML issue templates, `pyproject.toml`, `uv`, `hatchling`.

**Spec:** `docs/plans/2026-11-24-public-repo-polish-design.md`

## Global Constraints

- Python `>=3.12`; use `uv` for all project commands.
- Offline gates must pass after every task: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.
- Never hand-edit `src/python_ise/generated/`.
- Never contact a Cisco ISE appliance and never use credentials during this work.
- Never put real passwords, real IPs, real hostnames, internal URLs, ticket IDs, or colleague names in files or commit messages.
- Commit identity: `SoloSunset <mathias@mdkp.dk>`.
- No push until a human explicitly approves the finished branch.

## Review Focus

- Company-associated metadata returning through docs or package fields — verify with the high-signal `git grep` in every task.
- Generated-code drift from docs-only edits — verify with `python_ise.generate --check` in every task.
- README claiming coverage the repository does not have — verify the coverage wording against `tests/test_sdk_coverage.py` in Task 2.
- Contributors being told to use a live appliance or paste secrets — verify `CONTRIBUTING.md` contains explicit no-live-appliance and no-credentials rules in Task 3.
- Security reporters using public issues — verify `SECURITY.md` and issue-template config point to private reporting in Task 4.

---

### Task 1: License and package metadata

**Files:**
- Create: `LICENSE`
- Modify: `pyproject.toml`

**Interfaces:**
- Consumes: nothing.
- Produces: `LICENSE`; project metadata fields `license`, `classifiers`, `keywords`, and `urls` that later documentation links to.

- [ ] **Step 1: Add the MIT license**

Create `LICENSE` with the standard MIT text and copyright line `Copyright (c) 2026 SoloSunset`.

- [ ] **Step 2: Add package metadata**

In `pyproject.toml`, add these fields under `[project]`:

```toml
license = { file = "LICENSE" }
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
]
keywords = ["cisco", "ise", "ers", "mnt", "sdk"]
urls = { Homepage = "https://github.com/Solosunset/python-ise", Issues = "https://github.com/Solosunset/python-ise/issues", Repository = "https://github.com/Solosunset/python-ise" }
```

Keep the existing name, version, description, readme, authors, Python floor, dependencies, dependency groups, and hatch build settings unchanged.

- [ ] **Step 3: Verify metadata and gates**

Run:

```bash
uv build --wheel
uv run pytest -q
uv run python -m python_ise.generate --check
# High-signal leak check over HEAD: company email domain, internal host
# substring, home-path prefix, and password-literal pattern. The exact regex is
# intentionally not written here so this document does not match its own scan.
# Expect no matches.
```

Expected: wheel builds, 142 tests pass, generate check passes, grep prints nothing.

Note: use `uv build --wheel`, not `uv build`. The full build has a **pre-existing** hatchling `force-include` bug (confirmed on base `4283bf3`): the sdist flattens `src/` paths, so building the wheel from the sdist fails with `Forced include not found: .../src/python_ise/manifest/ers.yaml`. Direct wheel builds and all offline gates are unaffected. Fix the sdist packaging before adding `uv build` to CI in Phase 2.

- [ ] **Step 4: Commit**

```bash
git add LICENSE pyproject.toml
git commit -m "docs: add MIT license and package metadata"
```

### Task 2: Rewrite the README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: license and project URLs from Task 1; coverage facts from `tests/test_sdk_coverage.py`.
- Produces: a README with the required sections used by Tasks 3 and 4 for links.

- [ ] **Step 1: Confirm the coverage fact before writing**

Run:

```bash
grep -n 'RESOURCE_TAILS\|assert' tests/test_sdk_coverage.py | head -20
grep -c '^    def ' src/python_ise/generated/ers_read.py
```

Expected: the test carries the sanitized 69-tail inventory; generated method count is greater than 200. Use the phrase "all 69 SDK resource tails are covered" in the README, not "Some ERS calls".

- [ ] **Step 2: Rewrite `README.md`**

Replace the whole file with a concise README containing, in this order:

1. `# python-ise` and one-sentence overview.
2. CI badge pointing to `https://github.com/Solosunset/python-ise/actions/workflows/generated-drift.yml/badge.svg`.
3. `## Status`: full MnT parity, all 69 ERS SDK resource tails covered, no OpenAPI support.
4. `## Install`: `uv add "git+https://github.com/Solosunset/python-ise.git"` and the `pip install git+...` equivalent.
5. `## Quickstart`: `MNT` and `ERS` examples that read `ISE_NODE`, `ISE_USER`, and `ISE_PASS` from `os.environ`; use `ise.example.invalid` for the host example.
6. `## Result contract`: the existing `{'success', 'response', 'error'}` shape.
7. `## Generated code`: manifest-driven rule and both generation commands, with the explicit never-hand-edit rule.
8. `## Testing`: offline gate commands and the statement that tests never contact a real appliance.
9. `## Contributing`: link to `CONTRIBUTING.md`.
10. `## Security`: link to `SECURITY.md` and say not to open public issues for secrets.
11. `## License`: MIT, link to `LICENSE`.
12. `## Credits`: attribution to the original upstream project already named in the current README.

Do not include real hosts, real IPs, real usernames, real passwords, internal URLs, or ticket IDs.

- [ ] **Step 3: Verify README sections and gates**

Run:

```bash
for s in '^# python-ise' '^## Status' '^## Install' '^## Quickstart' '^## Result contract' '^## Generated code' '^## Testing' '^## Contributing' '^## Security' '^## License'; do
  grep -qE "$s" README.md || { printf 'missing section: %s\n' "$s"; exit 1; }
done
grep -n 'ISE_PASS\|os.environ\|ise.example.invalid\|all 69 SDK resource tails' README.md
uv run pytest -q
uv run python -m python_ise.generate --check
```

Expected: every section present, env-var example and coverage phrase present, tests pass, generate check passes.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for public users"
```

### Task 3: Contributor guide

**Files:**
- Create: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: README contract and generated-code rule from Task 2; existing `docs/agent-runbook.md`.
- Produces: the contribution workflow referenced by the README.

- [ ] **Step 1: Write `CONTRIBUTING.md`**

Include these required sections and exact rules:

- `## Getting started`: clone the public repo, `uv sync --dev`, run both offline gates.
- `## Adding an endpoint family`: manifest entry → minimal credential-free fixture → failing test → implementation → regenerate → full gates.
- `## Hard rules`: one resource family per change; never hand-edit `src/python_ise/generated/`; never contact a real appliance; never commit real credentials, hostnames, IPs, or logs.
- `## Pull request checklist`: gates pass, generated output matches manifest, diff touches only the intended family, commit message has no sensitive values.
- `## Questions`: use Discussions for open questions and Issues for actionable bugs or feature requests.

- [ ] **Step 2: Verify guide rules and gates**

Run:

```bash
grep -qF 'uv sync --dev' CONTRIBUTING.md
grep -qF 'never hand-edit' CONTRIBUTING.md
grep -qF 'never contact a real appliance' CONTRIBUTING.md
grep -qF 'Discussions' CONTRIBUTING.md
uv run pytest -q
uv run python -m python_ise.generate --check
# High-signal leak check over HEAD: company email domain, internal host
# substring, home-path prefix, and password-literal pattern. The exact regex is
# intentionally not written here so this document does not match its own scan.
# Expect no matches.
```

Expected: all greps succeed, gates pass, high-signal grep prints nothing.

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add contributor guide"
```

### Task 4: Security policy and issue templates

**Files:**
- Create: `SECURITY.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/question.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`

**Interfaces:**
- Consumes: project URLs from Task 1 and README links from Task 2.
- Produces: private-reporting instructions and valid GitHub issue templates.

- [ ] **Step 1: Write `SECURITY.md`**

State that vulnerabilities and anything containing credentials, tokens, real hostnames, real IPs, appliance logs, or customer data must be reported privately through GitHub's **Report a vulnerability** flow on the repository Security tab. Say that public issues are for non-sensitive bugs and feature requests only.

- [ ] **Step 2: Write issue templates**

Create three YAML templates with `name`, `description`, `title`, `labels`, and `body` fields:

- `bug_report.yml`: asks for version, Python version, minimal reproduction, expected behavior, actual behavior, and sanitized traceback; includes a checkbox confirming no secrets or real host data are included.
- `feature_request.yml`: asks for problem statement, proposed API or behavior, and alternatives considered.
- `question.yml`: asks for what the user tried and where they got stuck; directs open-ended discussion to Discussions.

Create `config.yml` with `blank_issues_enabled: false` and a `contact_links` entry named `Questions and discussion` pointing to `https://github.com/Solosunset/python-ise/discussions`.

- [ ] **Step 3: Verify YAML, links, and gates**

Run:

```bash
uv run python - <<'PY'
import yaml
from pathlib import Path
for path in sorted(Path(".github/ISSUE_TEMPLATE").glob("*.yml")):
    yaml.safe_load(path.read_text())
    print(f"valid: {path}")
PY
grep -qF 'Report a vulnerability' SECURITY.md
grep -qF 'blank_issues_enabled: false' .github/ISSUE_TEMPLATE/config.yml
grep -qF 'python-ise/discussions' .github/ISSUE_TEMPLATE/config.yml
uv run pytest -q
uv run python -m python_ise.generate --check
```

Expected: all four templates parse, both greps succeed, gates pass.

- [ ] **Step 4: Commit**

```bash
git add SECURITY.md .github/ISSUE_TEMPLATE
git commit -m "docs: add security policy and issue templates"
```

## Operational checklist — not automatable in this branch

These settings still need a human with repository admin access:

1. Settings → General → Features: enable **Discussions**; keep **Issues** enabled.
2. Settings → Security → Private vulnerability reporting: enable it.
3. Settings → General: set description and topics `cisco`, `ise`, `ers`, `mnt`, `python`, `sdk`.
4. Settings → Branches: protect `main` and require the `generated-drift` check.
5. Confirm the public repo URL renders `https://github.com/Solosunset/python-ise` and the README links resolve.

## Out of scope for this plan

Phase 2 (CI polish: secret scanning, `uv build`, Python matrix, optional `ruff`) and Phase 3 (tag-triggered PyPI release with Trusted Publishing) get separate plans after this branch is reviewed and merged.
