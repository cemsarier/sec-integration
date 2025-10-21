from core.client import SECClient
from core.constants import COMPANIES_TO_CIK
from core.handler import SECReader
from settings import OUTPUT_DIR, SEC_USER_AGENT

# Initialize SEC client
sec_client = SECClient(user_agent=SEC_USER_AGENT)
reader = SECReader(sec_client, OUTPUT_DIR)

# Fetch and save latest 10-K filings for each company
for company, cik in COMPANIES_TO_CIK.items():
    print(f"Fetching latest 10-K for {company} (CIK: {cik})...")

    # All submissions
    submissions = reader.fetch_all_company_submissions(cik)

    # Get latest 10-K filing summary
    latest_10k_summary = reader.get_latest_filing_summary_from_submissions(
        submissions, form_type="10-K"
    )

    # Fetch the latest filing document
    latest_10k_filing_html = reader.get_filing_document(cik, latest_10k_summary)

    # Save filing and create PDF
    result_path = reader.save_filing(cik, latest_10k_filing_html, latest_10k_summary)
    pdf_path = reader.create_pdf_from_filing(result_path)
