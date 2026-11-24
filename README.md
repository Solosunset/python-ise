# Usecases
This module has (will have) preconfigured functions for most of the available API calls to a Cisco ISE appliance, as well as some nice to have features like getting *all* endpoints.

## Credits
The initial code for this project comes from https://github.com/falkowich/pyise-ers.

# Contract
The shared contract for results, generated methods, fixtures, and agent workflow is in [docs/contracts/api-contract.md](docs/contracts/api-contract.md). Agents follow [docs/agent-runbook.md](docs/agent-runbook.md); generated files are refreshed with `python -m python_ise.generate` and checked in CI with `python -m python_ise.generate --check`.

# Current progress
- Full parity for all MnT calls
- Some ERS calls
- No OpenAPI calls

# Usage
There are (will be) 3 available classes ERS, MNT and OpenAPI.

See available calls at https://developer.cisco.com/docs/identity-services-engine/latest/cisco-ise-api-framework/ under "API Reference", for MnT calls go to https://developer.cisco.com/docs/identity-services-engine/v1/introduction-to-the-monitoring-rest-api/.

All calls *should* return a result dictionary like so:
```python
{'success': bool, 'response': dict|list|str, 'error': str|int}
```

In the event of an error, 'success' will be `False`, 'response' will be the json/xml parsed error message from ISE, 'error' will be the http status code like `500` or `401`

## MnT
**quickstart**
```python
from python_ise import python_ise

ise_mnt = python_ise.MNT(
    'ISE_MnT_Node', # hostname or IPaddress eg. my_ise_mnt01.myorg.local
    'username', # Username of user with MnT API access
    '<your-password>', # User's password
)

print(ise_mnt.get_activeCount())
```

**output**
```python
{'success': True, 'response': {'count': '9999'}, 'error': ''}
```

## ERS
**quickstart**
```python
from python_ise import python_ise

ise_mnt = python_ise.ERS(
    'ISE_pan_Node', # management interface fqdn or IPaddress eg. ise.myorg.local
    'username', # Username of user with ERS API access
    '<your-password>', # User's password
)

print(ise_mnt.get_endpoint_macAddress('aa:bb:cc:12:34:56'))
```

**output**
```python
{'success': True, 'response': {'id': 'aaaaaaaa-bbbbb-1111-2222-000h46090e11', 'name': 'aa:bb:cc:12:34:56', 'description': '', 'mac': 'aa:bb:cc:12:34:56', 'profileId': '', 'staticProfileAssignment': False, 'staticProfileAssignmentDefined': True, 'groupId': 'aaaaaaaa-bbbbb-1111-2222-000h46090e22', 'staticGroupAssignment': True, 'staticGroupAssignmentDefined': True, 'portalUser': '', 'identityStore': '', 'identityStoreId': '', 'customAttributes': {'customAttributes': {'Attribute1': ''}}, 'link': {'rel': 'self', 'href': 'https://ISE_pan_Node.myorg.local:9060/ers/config/endpoint/name/aa:bb:cc:12:34:56', 'type': 'application/json'}}, 'error': ''}
```