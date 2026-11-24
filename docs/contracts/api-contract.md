# ISE API Wrapper Contract

This document is the shared contract for the manifest-driven ISE API wrapper. Every agent and every change must obey it.

## Result contract

Every call returns `{'success': bool, 'response': dict|list|str, 'error': str|int}`. Extra keys allowed only for pagination (`total`, `nextPage`, `prev`). MNT active-session list methods return a list in `response` (Task 5); ERS methods return `dict` or `str`.

In the event of an error, `success` is `False`, `response` is the parsed error message from ISE, and `error` is the HTTP status code (for example `500` or `401`).

## Generated read operations

Only four read shapes are generated: `list`, `by_id`, `by_name`, `version_info`. Their exact signatures are:

- `get_<name>_id(OID)` — look up a resource by object id; the legacy `_oid_test` guard raises `InvalidOID` on a bad id and must be preserved.
- `get_<name>_name(name)` — look up a resource by name.
- `get_<plural>(filter=None, size=20, page=1)` when the spec has `list_signature: "filter_size_page"` (the default), or `get_<plural>(size=20, page=1, *, filter=None)` when the spec has `list_signature: "size_page_filter"`. Both keep the default `size=20`; the second preserves the legacy positional `(size, page)` calling convention required by backward compatibility. The manifest field selects the shape — never infer it — and callers should pass `filter` by keyword in either case.
- `get_<name>_versionInfo()` — resource version info.

## Manifest and wrapper keys

Wrapper keys come from the manifest. Every wrapper key in the manifest must cite its source in the spec's `notes`: a fixture's top-level key or a Cisco ERS doc reference. Copying an unverified key from an existing method body is not sufficient.

Removing a hand-written read method must not remove extra behavior it carried (OID validation, raised exceptions, different path, extra result keys). Declare that behavior in the manifest (`validate_oid: true` for the `_oid_test`/`InvalidOID` guard, or `special: true` to keep a method hand-written); the generator preserves declared behavior and never silently drops it.

## Tests and fixtures

No test may contact a real ISE appliance. Use recorded JSON/XML fixtures and mocked HTTP only. Fixtures never contain credentials.

Every new resource requires a fixture. The fixture's top-level key is a valid source for that resource's manifest wrapper key.

## Agent workflow

Agents work one resource family at a time from the manifest. Do not spawn one agent per endpoint; irregular endpoints get their own task with a fixture.
