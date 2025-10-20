import os
from typing import Optional, Dict, TypedDict, Any
from core.client import SECClient
from core import utils


class LatestFilingSummary(TypedDict):
    form: str
    accessionNumber: str
    primaryDocument: str
    filingDate: str


class Reader_10K:
    def __init__(self, SEC_client: SECClient, output_path: str):
        self.SEC_client = SEC_client
        self.output_path = output_path
        utils.create_dir(self.output_path)

    def fetch_all_company_submissions(self, cik: str) -> Any:
        """
        Fetch company submissions JSON for the given CIK.
        """
        return self.SEC_client.get_company_submissions(cik)

    @staticmethod
    def get_latest_filing_summary_from_submissions(
        submissions: Dict, form_type: str = "10-K"
    ) -> Optional[LatestFilingSummary]:
        """
        From the 'recent filings' section of the given submissions,
        return the most recent filing of the given type.
        """
        filings = submissions.get("filings", {}).get("recent", {})

        forms = filings.get("form", [])
        accessions = filings.get("accessionNumber", [])
        docs = filings.get("primaryDocument", [])
        dates = filings.get("filingDate", [])  # sorted by most recent first

        for idx, form in enumerate(forms):
            if form and form.upper().startswith(form_type.upper()):
                # NOTE: Assumes there is only one latest filing of this type implicitly
                return LatestFilingSummary(
                    form=form,
                    accessionNumber=accessions[idx],
                    primaryDocument=docs[idx],
                    filingDate=dates[idx],
                )
        return None

    def get_filing_document(self, cik: str, filing_summary: LatestFilingSummary) -> str:
        """
        Fetch company submissions html text for the given CIK and filing summary.
        """
        return self.SEC_client.get_filing_document(
            cik, filing_summary["accessionNumber"], filing_summary["primaryDocument"]
        )

    def save_filing(
        self, cik: str, filing_html: str, filing_summary: LatestFilingSummary
    ) -> str:
        """
        Save the 10-K filing for the given company to the specified output path.
        Returns the path to the saved file.
        """
        save_path = os.path.join(
            self.output_path, cik, f"10-K_{filing_summary['filingDate']}.html"
        )
        utils.save_html_to_file(filing_html, save_path)
        print(f"Saved latest 10-K to {save_path}")
        return save_path

    def create_pdf_from_filing(self, filing_html_path: str) -> Optional[str]:
        """
        Create a PDF from the 10-K filing HTML for the given company.
        Returns the path to the saved PDF file.
        """
        return utils.convert_html_to_pdf(filing_html_path)
