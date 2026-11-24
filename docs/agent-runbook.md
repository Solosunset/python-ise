# Agent runbook

Follow these steps in order for every manifest-driven wrapper change.

1. Read `docs/contracts/api-contract.md` (linked from the [README](../README.md)) and obey the result, generated-operation, fixture, and workflow rules.
2. Add or update manifest entries for **one resource family**, using the exact method names and wrapper keys from Cisco's ISE API docs. Cite each wrapper key's source in the spec's `notes` (fixture top-level key or doc reference).
3. Add a fixture and a failing test for the behavior before making it pass. Use mocked HTTP and credential-free fixtures only; never contact a real ISE appliance.
4. Run `uv run python -m python_ise.generate` to regenerate the modules from the manifest. Never hand-edit files under `src/python_ise/generated/`.
5. Run the targeted test first (for example `uv run pytest tests/test_generated_ers.py`), then the full suite with `uv run pytest`, plus `uv run python -m python_ise.generate --check` to confirm there is no drift.
6. Review the diff: reject any change touching an unrelated resource or helper. Generated output must match the manifest, and unrelated hand-written code must be untouched.
7. Commit the manifest, fixture, tests, and regenerated files together.

## Scope

Work on one resource family per session; spawning one agent session per endpoint is forbidden. Irregular endpoints get their own task with a fixture, not a one-off agent or an undocumented special case.
