from typing import Optional, Dict
from core.client import SECClient
from core import utils
from core.constants import COMPANIES_TO_CIK


class Reader_10K:
    def __init__(self, SEC_client: SECClient):
        self.SEC_client = SEC_client

    def fetch_company_submissions(self, cik: str) -> Dict:
        """
        Fetch company submissions JSON for the given CIK.
        """
        return self.SEC_client.get_company_submissions(cik)

    def get_latest_filing_from_submissions(
        self, submissions: Dict, form_type: str = "10-K"
    ) -> Optional[Dict]:
        """
        From the 'recent filings' section, return the most recent filing of the given type.
        """
        filings = submissions.get("filings", {}).get("recent", {})

        forms = filings.get("form", [])
        accessions = filings.get("accessionNumber", [])
        docs = filings.get("primaryDocument", [])
        dates = filings.get("filingDate", [])  # sorted by most recent first

        # Available keys:  ['accessionNumber', 'filingDate', 'reportDate', 'acceptanceDateTime',
        # 'act', 'form', 'fileNumber', 'filmNumber', 'items', 'core_type', 'size', 'isXBRL', 'isInlineXBRL',
        # 'primaryDocument', 'primaryDocDescription']

        # TODO: make sure the dates are sorted most recent first

        for idx, form in enumerate(forms):
            if form and form.upper().startswith(form_type.upper()):
                # NOTE: Assumes there is only one latest filing of this type implicitly
                return {
                    "form": form,
                    "accessionNumber": accessions[idx],
                    "primaryDocument": docs[idx],
                    "filingDate": dates[idx],
                }
        return None

    def fetch_and_download_latest_10k(
        self, company: str, output_path: str
    ) -> Optional[str]:
        """
        Download the latest 10-K filing for the given CIK and save it to the specified output path.
        Returns the path to the saved file or None if no 10-K found.
        """
        cik = COMPANIES_TO_CIK.get(company)
        if not cik:
            print(f"CIK not found for company: {company}")
            return None

        submissions = self.fetch_company_submissions(cik)
        latest_filing = self.get_latest_filing_from_submissions(
            submissions, form_type="10-K"
        )
        if not latest_filing:
            print(f"No 10-K filing found for CIK {cik}.")
            return None

        accession = latest_filing["accessionNumber"]
        primary_doc = latest_filing["primaryDocument"]

        html_text = self.SEC_client.get_filing_document(cik, accession, primary_doc)
        save_path = f"{output_path}/{company}_10-K_{latest_filing['filingDate']}.html"
        utils.save_html_to_file(html_text, save_path)
        print(f"Saved latest 10-K to {output_path}")
        return output_path
