"""Render the deterministic generated modules from the manifest."""

import argparse
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from python_ise.spec import ERS_MANIFEST, EndpointSpec, load_specs

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
GENERATED_DIR = Path(__file__).resolve().parent / "generated"
OUTPUT = GENERATED_DIR / "ers_read.py"
ALIASES_OUTPUT = GENERATED_DIR / "aliases.py"
KNOWN_OPERATIONS = frozenset({"list", "by_id", "by_name", "version_info"})
KNOWN_LIST_SIGNATURES = frozenset({"filter_size_page", "size_page_filter"})


def _unknown_operation(spec_name: str, operation: str) -> None:
    """Fail loudly if a manifest operation has no template branch."""
    raise ValueError(f"unknown operation {operation!r} for spec {spec_name!r}")


def _validate_specs(specs: list[EndpointSpec]) -> None:
    """Reject manifests that would silently drop or shadow a public method."""
    seen: dict[str, str] = {}
    for spec in specs:
        if spec.list_signature not in KNOWN_LIST_SIGNATURES:
            raise ValueError(
                f"unknown list_signature {spec.list_signature!r} for spec {spec.name!r}"
            )
        for operation, method_name in spec.methods.items():
            if operation not in KNOWN_OPERATIONS:
                raise ValueError(
                    f"unknown operation {operation!r} for spec {spec.name!r}"
                )
            if not method_name.isidentifier():
                raise ValueError(
                    f"invalid generated method name {method_name!r} for spec {spec.name!r}"
                )
            if method_name in seen:
                raise ValueError(
                    f"duplicate generated method name {method_name!r} in specs "
                    f"{seen[method_name]!r} and {spec.name!r}"
                )
            seen[method_name] = spec.name


def _environment() -> Environment:
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.globals["unknown_operation"] = _unknown_operation
    return environment


def render(specs: list[EndpointSpec]) -> str:
    """Render all four read shapes from the given endpoint specifications."""
    _validate_specs(specs)
    return _environment().get_template("ers_read.py.j2").render(specs=specs)


def render_aliases(specs: list[EndpointSpec]) -> str:
    """Render the static compatibility registry from the endpoint specifications."""
    _validate_specs(specs)
    return _environment().get_template("aliases.py.j2").render(specs=specs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when a generated file differs from the manifest",
    )
    args = parser.parse_args(argv)

    specs = load_specs(ERS_MANIFEST)
    expected_files = {
        OUTPUT: render(specs),
        ALIASES_OUTPUT: render_aliases(specs),
    }
    if args.check:
        stale = [
            path
            for path, expected in expected_files.items()
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        for path in stale:
            print(
                f"{path} is out of date; run python -m python_ise.generate",
                file=sys.stderr,
            )
        return 1 if stale else 0

    for path, expected in expected_files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
