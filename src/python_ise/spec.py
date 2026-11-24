"""Schema and loader for the declarative ERS endpoint manifest."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


ERS_MANIFEST: Path = Path(__file__).parent / "manifest" / "ers.yaml"


@dataclass
class EndpointSpec:
    """One ERS resource and the exact public methods that serve it."""

    name: str
    path: str
    wrapper: str
    methods: dict[str, str]
    version: str
    plural: str = ""
    legacy_names: list[str] = field(default_factory=list)
    validate_oid: bool = False
    list_signature: str = "filter_size_page"
    notes: str = ""
    special: bool = False


def load_specs(path: Path) -> list[EndpointSpec]:
    """Load a YAML manifest as a list of endpoint specifications."""
    entries = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return [EndpointSpec(**entry) for entry in entries]
