# python-ise

A small Python library for Cisco ISE's ERS and Monitoring (MnT) REST APIs, with manifest-generated ERS wrappers and a consistent result contract.

[![generated-drift](https://github.com/Solosunset/python-ise/actions/workflows/generated-drift.yml/badge.svg)](https://github.com/Solosunset/python-ise/actions/workflows/generated-drift.yml)

## Status

- Full parity for all MnT calls.
- Coverage: all 69 SDK resource tails are covered by generated ERS wrappers (201 generated methods).
- No OpenAPI support yet.

The API reference is published by Cisco under [ISE API framework](https://developer.cisco.com/docs/identity-services-engine/latest/cisco-ise-api-framework/) and [Monitoring REST API](https://developer.cisco.com/docs/identity-services-engine/v1/introduction-to-the-monitoring-rest-api/).

## Install

```bash
uv add "git+https://github.com/Solosunset/python-ise.git"
```

or with pip:

```bash
pip install "git+https://github.com/Solosunset/python-ise.git"
```

Python 3.12 or newer is required.

## Quickstart

Credentials and the node address are read from the environment so nothing sensitive ends up in source code:

```bash
export ISE_NODE='ise.example.invalid'
export ISE_USER='your-api-user'
export ISE_PASS='your-api-password'
```

Monitoring (MnT):

```python
import os

from python_ise import python_ise

mnt = python_ise.MNT(
    os.environ["ISE_NODE"],
    os.environ["ISE_USER"],
    os.environ["ISE_PASS"],
)

print(mnt.get_activeCount())
# {'success': True, 'response': {'count': '9999'}, 'error': ''}
```

ERS:

```python
import os

from python_ise import python_ise

ers = python_ise.ERS(
    os.environ["ISE_NODE"],
    os.environ["ISE_USER"],
    os.environ["ISE_PASS"],
)

print(ers.get_endpoint_macAddress("aa:bb:cc:12:34:56"))
# {'success': True, 'response': {'id': '...', 'name': 'aa:bb:cc:12:34:56', ...}, 'error': ''}
```

## Result contract

Every call returns the same shape:

```python
{"success": bool, "response": dict | list | str, "error": str | int}
```

On success, `success` is `True`, `response` holds the parsed JSON/XML result, and `error` is empty. On failure, `success` is `False`, `response` holds the parsed error body from ISE, and `error` is the HTTP status code such as `500` or `401`.

The full contract for results, generated operations, fixtures, and the agent workflow is in [docs/contracts/api-contract.md](docs/contracts/api-contract.md).

## Generated code

ERS wrappers are generated from `src/python_ise/manifest/ers.yaml` using the templates in `src/python_ise/templates/`. Never hand-edit anything under `src/python_ise/generated/`.

```bash
uv run python -m python_ise.generate        # regenerate
uv run python -m python_ise.generate --check  # verify no drift
```

## Testing

The test suite is fully offline: it uses mocked HTTP and credential-free fixtures and never contacts a real ISE appliance.

```bash
uv sync --dev
uv run pytest -q
uv run python -m python_ise.generate --check
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and hard rules.

## Security

Do not open public issues for vulnerabilities or anything containing credentials, tokens, real hostnames, real IPs, appliance logs, or customer data. See [SECURITY.md](SECURITY.md) for private reporting.

## License

GPLv2 — see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

## Credits

The initial code for this project comes from [falkowich/ise](https://github.com/falkowich/ise), with earlier contributors credited by that project including `bobthebutcher`, `mpenning`, `karrots`, and `msom`. See [NOTICE.md](NOTICE.md) for the full provenance and licensing attribution.
