import pytest

from core.client import SECClient


@pytest.fixture(scope="session")
def client():
    """Create a single SECClient instance for all integration tests."""
    user_agent = "QuartrDataAutomationCase/1.0 (integration@test.com)"
    return SECClient(user_agent)
