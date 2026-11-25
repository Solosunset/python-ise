# Public Repository Polish Design

> This records the approved direction for making the published `python-ise` repository welcoming to outside contributors. Phase 1 is implemented by `2026-11-24-contributor-ready-basics.md`; later phases get their own plans.

**Intent:** Keep the public repository useful and low-risk for other people to report issues, ask questions, and contribute code, without changing library behavior or reintroducing sensitive material.

**Goals:**

- Make the README describe what the library actually does today.
- Give the repository a clear license and package metadata.
- Tell contributors exactly how to add an endpoint family without touching generated code or live appliances.
- Give security reporters a private route instead of public issue text.
- Provide issue templates and a place for open-ended questions.
- Leave CI and release work as separately planned follow-ups.

**Non-goals:**

- No changes to runtime behavior, generated modules, manifest, fixtures, or tests.
- No PyPI release or release automation in this phase.
- No real appliance contact, credentials, real hostnames, real IPs, internal URLs, ticket IDs, or colleague names in repository files or commit messages.
- No reuse of the old local workspace; work happens on a branch of the public clone.

**Constraints:**

- Python `>=3.12`; `uv` is the project tool.
- Generated files under `src/python_ise/generated/` are never hand-edited.
- Offline gate commands must keep passing: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.
- Commit identity for new commits: `SoloSunset <mathias@mdkp.dk>`.
- Public repo canonical SSH remote: `git@github.com:Solosunset/python-ise.git`.
- Plan documents live in `docs/plans/` because `docs/superpowers/` was deliberately removed from the published tree.

**Approaches considered:**

- **A — Contributor-ready public repo (chosen).** Add license, accurate README, contributing guide, security policy, and issue templates now. This matches the stated goal of letting people flag issues and comment.
- **B — Minimal polish.** License plus README only. Cheaper, but leaves contributors without a safe workflow and leaves security reports exposed in public issues.
- **C — PyPI-ready immediately.** Adds release automation now. Rejected because it introduces token/trusted-publishing work unrelated to the immediate goal.

**Decisions:**

- License: MIT, with copyright holder `SoloSunset`.
- Questions and open-ended comments belong in GitHub Discussions; actionable bugs and feature requests belong in Issues.
- Security issues must be reported privately through GitHub's private vulnerability reporting flow, documented in `SECURITY.md`.
- CI stays as the existing single `generated-drift.yml` workflow until Phase 2.
- Phase 2 will add secret scanning, `uv build`, a Python matrix, and optional `ruff`; Phase 3 will add tag-triggered PyPI release with Trusted Publishing.

**What is left to the implementer:**

- Exact badge placement and final README wording, provided all required sections and checks remain present.
- Exact issue-template field wording, provided the templates parse as YAML and ask for reproduction, environment, and logs.
