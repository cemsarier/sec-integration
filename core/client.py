"""A simple SEC EDGAR API client."""

import time
from typing import Any

import requests

from core import utils


class SECClient:
    BASE_URL = "https://data.sec.gov"
    ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data"
    RETRY_COUNT = 3
    RETRY_DELAY = 1.0  # seconds between retries
    TIMEOUT = 10.0  # seconds for HTTP requests

    def __init__(self, user_agent: str):
        self._validate_user_agent(user_agent)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "application/json, text/plain, */*",
            }
        )

    @staticmethod
    def _validate_user_agent(user_agent: str) -> None:
        """
        Validate the SEC user agent string.
        :param user_agent:
        :return:
        """
        if not user_agent or "@" not in user_agent:
            raise ValueError(
                "SEC user_agent must include a valid contact (name + email), e.g. 'MyApp/1.0 (me@company.com)'"
            )

    def _get(self, url: str) -> requests.Response:
        """GET request with basic retry and rate-limiting."""
        for attempt in range(self.RETRY_COUNT):
            try:
                resp = self.session.get(url, timeout=self.TIMEOUT)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                print(f"[WARN] Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(self.RETRY_DELAY)
        raise RuntimeError(f"Failed to fetch after {self.RETRY_COUNT} attempts: {url}")

    def get_company_submissions(self, cik: str) -> Any:
        """Fetch company submissions JSON."""
        padded = utils.pad_cik(cik)
        url = f"{self.BASE_URL}/submissions/CIK{padded}.json"
        resp = self._get(url)
        return resp.json()

    def get_filing_document(self, cik: str, accession: str, primary_doc: str) -> str:
        """
        Download the HTML text of the filing document.
        """
        cleaned_acc = accession.replace("-", "")
        no_zero_cik = str(int(cik))
        url = f"{self.ARCHIVE_URL}/{no_zero_cik}/{cleaned_acc}/{primary_doc}"
        resp = self._get(url)
        return resp.text
