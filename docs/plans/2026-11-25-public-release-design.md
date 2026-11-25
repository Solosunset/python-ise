# Public Release Design (GPLv2)

> Draft for approval. This supersedes the MIT licensing decision recorded in `2026-11-24-public-repo-polish-design.md` after reviewing the upstream project's GPLv2 license and the derivation of the current code.

**Intent:** Publish `python-ise` to TestPyPI and then PyPI as an openly licensed, commercially usable GPLv2 wrapper for Cisco ISE ERS and MNT, with accurate provenance, a working source distribution, and a repeatable release path that cannot publish accidentally.

**Background:**

- The existing package `ISE` on PyPI is at `0.1.2` and points at `falkowich/ise`.
- The upstream repository carries the GNU General Public License, version 2.
- The current `python-ise` implementation is derived from that work: the module docstring, helper names, URL construction, response handling, and API shape are visibly related.
- TestPyPI already has a stale `python-ise 0.1.4` release. Real PyPI does not currently have the name `python-ise`.
- `uv build` currently fails when building a wheel from the sdist because Hatchling's forced includes are absent from the sdist staging tree.
- The package description currently claims OpenAPI support, but no OpenAPI wrapper has been implemented.

**Goals:**

- Make the license and provenance accurate before publication.
- Keep the library usable and sellable commercially under terms that match the upstream source.
- Replace the stale TestPyPI release with a newer, clearly documented version.
- Claim the free PyPI name only after the TestPyPI release has been verified.
- Fix the sdist/wheel build so both artifacts can be uploaded and installed.
- Add a release workflow that is manual, explicit, and reversible by omission.
- Keep all tests and gates fully offline.
- Correct package metadata so the first release claims only the ERS and MNT support that actually exists.

**Non-goals:**

- No clean-room rewrite and no relicensing to MIT, 0BSD, or public-domain-style terms.
- No attempt to contact or obtain new permission from upstream authors.
- No OpenAPI wrapper in the first release; that is a follow-up.
- No publish to TestPyPI or PyPI without separate explicit user approval.
- No push, PR, tag, remote, or GitHub setting change without explicit user approval.
- No real passwords, IPs, hostnames, internal URLs, ticket IDs, or colleague names in published files or commit messages.
- No hand-edits to files under `src/python_ise/generated/`.

**Constraints:**

- Python `>=3.12`; `uv` is the project tool.
- Offline gates must stay green: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.
- Commit identity for new commits: `SoloSunset <mathias@mdkp.dk>`.
- Public repo canonical SSH remote: `git@github.com:Solosunset/python-ise.git`.
- Plan documents live in `docs/plans/`; `docs/superpowers/` stays out of the published tree.
- Upstream is treated as GPL-2.0-only unless an explicit "or later" grant is found.
- GPLv2 permits commercial use and sale, but anyone distributing this code or derivatives must comply with the GPLv2 source, notice, and licensing obligations.

**Approaches considered:**

- **A — Publish as GPLv2 with accurate notices (chosen).** Keep the current implementation, replace the MIT license with GPLv2, add explicit provenance and third-party notices, fix the build, and release `0.2.0`. This matches the source derivation and allows commercial use without overstating rights.
- **B — Seek MIT/0BSD relicensing from upstream authors.** Would permit fewer downstream obligations, but depends on several historical contributors and has no guaranteed outcome. Rejected as a prerequisite for release.
- **C — Rebuild from public Cisco API docs and publish permissively.** Would give the cleanest "no restrictions" story, but is substantially more work and is unnecessary now that GPLv2 is acceptable. Deferred.
- **D — Publish the current MIT tree unchanged.** Fast, but internally contradictory: it claims unrestricted rights over code visibly derived from a GPLv2 work. Rejected.
- **E — Do not publish.** Avoids licensing work, but does not meet the goal of replacing the stale `ISE` package. Rejected.

**Decisions:**

1. **License.** Replace `LICENSE` with the full GNU General Public License, version 2 text. Use SPDX identifier `GPL-2.0-only` in metadata and the PyPI classifier `License :: OSI Approved :: GNU General Public License v2 (GPLv2)`.
2. **Source headers.** Add a short GPLv2 notice to each Python source and template file. The notice identifies `SoloSunset` as the current maintainer and states that the work is derived from `falkowich/ise`; it does not claim exclusivity or original authorship of the upstream portions.
3. **Provenance.** Add `NOTICE.md` with factual upstream attribution: `falkowich/ise`, earlier contributors named in that project's README, and the GPLv2 license source. Update `README.md` so its License section says GPLv2 and its provenance section explains the relationship plainly.
4. **Version.** Use `0.2.0rc1` for TestPyPI and `0.2.0` for PyPI. This avoids the occupied `0.1.4` TestPyPI version and signals a real packaging/licensing change without implying a clean-room rewrite.
5. **Metadata.** Change the description to "Library to interact with Cisco ISE's ERS and MNT APIs". Keep OpenAPI out of keywords and classifiers until implemented.
6. **Build fix.** Adjust Hatch configuration so the sdist includes `src/python_ise/manifest/ers.yaml`, `src/python_ise/templates/*.j2`, `README.md`, `LICENSE`, and `NOTICE.md`, and so the wheel includes the manifest and templates. Verify both artifacts with `uv build` and `python -m twine check dist/*`.
7. **Release workflow.** Add `.github/workflows/publish.yml` with `workflow_dispatch` only. Inputs: `target` (`testpypi` or `pypi`) and `confirm` (must be `true`). The build job runs the offline gates, builds artifacts, runs `twine check`, and uploads a build artifact. Publishing jobs use GitHub Environments `testpypi` and `pypi` with OIDC Trusted Publishing via `pypa/gh-action-pypi-publish`.
8. **Manual control.** No tag-triggered publishing in the first version. A release happens only when a human deliberately dispatches the workflow after the user approves that specific release.
9. **Account setup.** The user must configure Trusted Publishers in TestPyPI and PyPI for owner `Solosunset`, repository `python-ise`, workflow `publish.yml`, and the matching environment names. Until then the workflow is build-only or will fail safely at the publish step.
10. **OpenAPI.** Track as a separate follow-up, targeted at `0.3.0`, with its own design and offline tests. Do not claim it in `0.2.0`.

**Implementation outline:**

- **Phase 1 — Licensing and metadata.** Replace `LICENSE`; add `NOTICE.md`; update README, `pyproject.toml`, and source headers. Run the offline gates.
- **Phase 2 — Build repair.** Fix Hatch sdist/wheel includes; verify generated files are regenerated from the packaged manifest and templates, not edited by hand.
- **Phase 3 — Release workflow.** Add the manual dispatch workflow and document the release procedure in `docs/` or `CONTRIBUTING.md`.
- **Phase 4 — TestPyPI release.** After explicit approval, bump to `0.2.0rc1`, dispatch the `testpypi` target, install from TestPyPI in a clean virtual environment, and verify import plus basic offline behavior.
- **Phase 5 — PyPI release.** After separate explicit approval and successful TestPyPI verification, bump to `0.2.0` and dispatch the `pypi` target.
- **Phase 6 — OpenAPI follow-up.** Design and implement a real OpenAPI wrapper, then publish `0.3.0`.

**Verification gates:**

- `uv run pytest -q` — expected 142 passing tests.
- `uv run python -m python_ise.generate --check` — no generated drift.
- `uv build` — produces both sdist and wheel.
- `python -m twine check dist/*` — metadata and README render cleanly.
- Inspect sdist and wheel file lists: manifest and templates present; no `docs/superpowers/`; no secrets, real hosts, real IPs, ticket IDs, or colleague names.
- Install the wheel in a clean virtual environment and import `python_ise` without network access.
- Check `git diff --check` and confirm no generated file was edited directly.
- Confirm every commit uses the approved identity and contains no sensitive strings.

**Release approvals:**

- Approval of this design authorizes implementation of Phases 1–3 only.
- A separate explicit approval is required before the TestPyPI dispatch in Phase 4.
- A further separate explicit approval is required before the PyPI dispatch in Phase 5.
- No remote push, PR, tag, release, repository setting, or package upload happens without the relevant approval.

**Risks and mitigations:**

- **GPLv2 obligations surprise downstream users.** Mitigated by prominent documentation in README, `NOTICE.md`, package metadata, and the license text.
- **Attribution is incomplete.** Mitigated by naming the upstream project and its credited contributors and by preserving GPLv2 notices.
- **Licensing claim still faces a challenge.** A license cannot prevent a lawsuit; accurate provenance and compliance remove the most obvious basis for one.
- **Trusted Publishing is misconfigured.** Mitigated by manual dispatch, environment protection, and a dry build job that always runs before publish.
- **Stale TestPyPI release confuses users.** Mitigated by publishing `0.2.0rc1` with corrected metadata and README.
- **OpenAPI is advertised but absent.** Mitigated by correcting the description before release and deferring OpenAPI to a real implementation.

**Open questions for the implementer to resolve during planning:**

- Confirm the exact source-file header wording, keeping it short and non-exclusive.
- Confirm the final Hatch include/exclude configuration after testing on both sdist and wheel targets.
- Confirm the exact GitHub Environment names used for Trusted Publishing.
