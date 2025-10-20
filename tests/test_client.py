import time
import pytest

from core import utils
from core.client import SECClient
from core.constants import COMPANIES_TO_CIK
from core.utils import compute_hash


@pytest.fixture(scope="session")
def client():
    """Create a single SECClient instance for all integration tests."""
    user_agent = "QuartrDataAutomationCase/1.0 (integration@test.com)"
    return SECClient(user_agent)


def test_get_company_submissions(client):
    """Integration: actually fetch Apple Inc. submissions from SEC."""
    company = "Apple"
    cik = COMPANIES_TO_CIK[company]
    data = client.get_company_submissions(cik)

    # Basic checks
    assert isinstance(data, dict)
    assert "filings" in data
    assert "recent" in data["filings"]
    assert "form" in data["filings"]["recent"]
    assert "accessionNumber" in data["filings"]["recent"]
    assert "primaryDocument" in data["filings"]["recent"]
    assert "filingDate" in data["filings"]["recent"]

    # Check that there are many filings
    assert len(data["filings"]["recent"]["form"]) > 1000
    time.sleep(0.5)  # respect SEC rate limits


def test_get_filing_document(client):
    """
    Fetch a known filing (Apple 2024-11-01 10-K) and verify that its HTML content
    is stable.
    """
    company = "Apple"
    cik = COMPANIES_TO_CIK[company]

    accession = "0000320193-24-000123"
    primary_doc = "aapl-20240928.htm"
    # filingDate = 2024-11-01

    html = client.get_filing_document(cik, accession, primary_doc)

    assert isinstance(html, str)
    assert "<html" in html.lower() or "<DOCUMENT" in html.upper()
    assert len(html) > 1000  # reasonably large HTML
    print(f"Fetched 10-K document for Apple ({len(html)} bytes).")

    # Check hash to ensure content consistency
    computed_hash = compute_hash(html)
    known_hash = "6ad1e7a88d990c23e91db8f381946b4cbf1954cf53407b38a40b358eaccb1d7e"
    assert computed_hash == known_hash
    print("Computed hash:", computed_hash)

    time.sleep(0.5)
