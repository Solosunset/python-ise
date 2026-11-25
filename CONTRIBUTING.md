# Contributing

Thanks for helping improve `python-ise`. This project wraps Cisco ISE APIs, so a few rules keep contributions safe and reviewable.

## Getting started

```bash
git clone https://github.com/Solosunset/python-ise.git
cd python-ise
uv sync --dev
uv run pytest -q
uv run python -m python_ise.generate --check
```

Both offline gates must pass before you start changing anything.

For the release procedure and approval requirements, see [docs/releases.md](docs/releases.md).

## Adding an endpoint family

1. Add or update the manifest entry in `src/python_ise/manifest/ers.yaml` for **one resource family**, using the exact method name and wrapper key from Cisco's ISE API docs. Cite the source in the entry's `notes`.
2. Add a minimal, credential-free fixture using mocked HTTP.
3. Write a failing test for the behavior you want.
4. Implement the behavior needed to make the test pass.
5. Regenerate the wrappers: `uv run python -m python_ise.generate`.
6. Run the full gates: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.

See [docs/agent-runbook.md](docs/agent-runbook.md) and [docs/contracts/api-contract.md](docs/contracts/api-contract.md) for the detailed workflow and result contract.

## Hard rules

- One resource family per change.
- Always regenerate from the manifest: never hand-edit anything under `src/python_ise/generated/`.
- Tests use mocks only: never contact a real appliance.
- Never commit real credentials, hostnames, IPs, or logs.
- Keep generated output deterministic and derived solely from the manifest.

## Pull request checklist

- [ ] `uv run pytest -q` passes.
- [ ] `uv run python -m python_ise.generate --check` passes.
- [ ] Generated output matches the manifest.
- [ ] The diff touches only the intended resource family and its tests/fixtures.
- [ ] No real password, IP, hostname, internal URL, ticket ID, or colleague name appears in files or the commit message.

## Questions

Use GitHub Discussions for open-ended questions and ideas. Use Issues for actionable bug reports and feature requests. For anything sensitive, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
