"""Optional namespaced facade over the flat ERS client."""

from collections.abc import Callable, Mapping
from typing import Any

from .generated.aliases import FACADE_SPECS
from .python_ise import ERS, MNT

_FACADE_OPERATIONS = {
    "get": "by_id",
    "list": "list",
    "by_name": "by_name",
    "version_info": "version_info",
}


class _ResourceFacade:
    """Expose only the read operations the manifest declares for one resource."""

    def __init__(self, client: ERS | None, methods: Mapping[str, str]) -> None:
        for attribute, operation in _FACADE_OPERATIONS.items():
            if operation in methods:
                setattr(self, attribute, self._delegator(client, methods[operation]))

    @staticmethod
    def _delegator(client: ERS | None, method_name: str) -> Callable[..., Any]:
        def delegate(*args: Any, **kwargs: Any) -> Any:
            if client is None:
                raise ValueError("ISEClient requires an ERS client for resource access")
            return getattr(client, method_name)(*args, **kwargs)

        return delegate


def _resource_property(plural: str, methods: Mapping[str, str]) -> property:
    def resource(self: "ISEClient") -> _ResourceFacade:
        return _ResourceFacade(self.ers, methods)

    return property(resource, doc=f"Namespaced access to {plural}.")


class ISEClient:
    """Namespaced view of ISE; the underlying clients stay available as .ers and .mnt."""

    def __init__(self, ers: ERS | None = None, mnt: MNT | None = None) -> None:
        self.ers = ers
        self.mnt = mnt


for _plural, _methods in FACADE_SPECS:
    setattr(ISEClient, _plural, _resource_property(_plural, _methods))
