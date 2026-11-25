# Releases

Publishing `python-ise` always requires explicit user approval for that specific release. Running the build or offline gates locally never uploads anything.

## Trusted Publisher prerequisites

Configure Trusted Publishing in both indexes before dispatching a release. The workflow stores no token or password: it uses OIDC through the GitHub environment whose name matches the index.

| Index | Owner | Repository | Workflow | Environment |
| --- | --- | --- | --- | --- |
| TestPyPI | `Solosunset` | `python-ise` | `publish.yml` | `testpypi` |
| PyPI | `Solosunset` | `python-ise` | `publish.yml` | `pypi` |

## TestPyPI release

1. With explicit approval for a TestPyPI release, bump the version in `pyproject.toml` to `0.2.0rc1`.
2. Run the offline gates: `uv run pytest -q` and `uv run python -m python_ise.generate --check`.
3. Commit the version change.
4. Dispatch the `publish` workflow manually with `target=testpypi` and `confirm=true`.
5. Install `python-ise==0.2.0rc1` from TestPyPI in a clean environment and verify that `import python_ise` succeeds.

## PyPI release

1. Only after the TestPyPI install is verified and a separate explicit approval is given for PyPI, bump the version in `pyproject.toml` to `0.2.0`.
2. Run the offline gates and commit the version change.
3. Dispatch the `publish` workflow manually with `target=pypi` and `confirm=true`.

No tags trigger publishing. The workflow has no `push` or tag trigger; a release happens only through the manual dispatch described above.
