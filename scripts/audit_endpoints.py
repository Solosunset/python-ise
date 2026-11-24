"""Inventory public methods in a Python module using the AST."""

import ast
from pathlib import Path


def audit_public_methods(
    path: Path, *, authoritative: set[str] | None = None
) -> dict[str, list[int]]:
    """Return public method names defined more than once, with their line numbers.

    Only methods declared directly on ``ClassDef`` nodes are considered; names
    beginning with an underscore are helpers and are ignored. ``authoritative``
    holds names whose canonical definition lives in another (generated) module:
    those names are not duplicates even when a stale copy remains here.
    """
    tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))
    definitions: dict[str, list[int]] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if item.name.startswith("_"):
                continue
            if authoritative is not None and item.name in authoritative:
                continue
            definitions.setdefault(item.name, []).append(item.lineno)

    return {name: lines for name, lines in definitions.items() if len(lines) > 1}
