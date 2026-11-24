import pytest
from tests.helpers import load_fixture  # noqa: F401 — re-exported for test modules

@pytest.fixture
def ers_client():
    from python_ise import ERS
    return ERS("ise.test.invalid", "u", "p", verify=False, disable_warnings=True)
