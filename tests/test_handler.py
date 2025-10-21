import os
import pickle

from core.handler import LatestFilingSummary, SECReader


def test_get_latest_filing_summary_from_submissions(client):
    # read the pickled submissions data
    output_path = os.path.join("tests", "test_data")
    with open(os.path.join(output_path, "apple_submissions_20251020.pkl"), "rb") as f:
        submissions = pickle.load(f)
    reader = SECReader(client, output_path=output_path)
    latest_10k = reader.get_latest_filing_summary_from_submissions(
        submissions, form_type="10-K"
    )
    assert latest_10k is not None
    assert latest_10k["form"] == "10-K"
    assert latest_10k["accessionNumber"] == "0000320193-24-000123"
    assert latest_10k["primaryDocument"] == "aapl-20240928.htm"
    assert latest_10k["filingDate"] == "2024-11-01"


def test_save_filing(client):
    output_path = os.path.join("tests", "test_data")
    reader = SECReader(client, output_path=output_path)
    with open(os.path.join(output_path, "Apple_10-K_2024-11-01.pkl"), "rb") as f:
        filing_html = pickle.load(f)
    filing_summary = LatestFilingSummary(
        form="10-K",
        accessionNumber="0000320193-24-000123",
        primaryDocument="aapl-20240928.htm",
        filingDate="2024-11-01",
    )
    save_path = reader.save_filing("0000320193", filing_html, filing_summary)
    assert save_path == os.path.join(output_path, "0000320193", "10-K_2024-11-01.html")


def test_create_pdf_from_filing(client):
    output_path = os.path.join("tests", "test_data")
    reader = SECReader(client, output_path=output_path)
    html_path = os.path.join(output_path, "0000320193", "10-K_2024-11-01.html")

    pdf_path = reader.create_pdf_from_filing(html_path)
    assert pdf_path is not None
    assert pdf_path == os.path.join(output_path, "0000320193", "10-K_2024-11-01.pdf")
