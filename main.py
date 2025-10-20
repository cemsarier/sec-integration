from core import utils
from core.handler import Reader_10K
from core.client import SECClient
from settings import SEC_USER_AGENT, OUTPUT_DIR

# Initialize SEC client
sec_client = SECClient(user_agent=SEC_USER_AGENT)
reader = Reader_10K(sec_client)

# List of companies to download 10-K filings for
companies = ["Apple"]
cik = "0000320193"  # CIK for Apple Inc.

# Initialzie the output directory
utils.create_dir(OUTPUT_DIR)
output_path = reader.fetch_and_download_latest_10k(
    company="Apple", output_path=OUTPUT_DIR
)
