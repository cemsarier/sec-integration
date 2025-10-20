"""Contains utility functions for the project."""

import os
import pdfkit
import hashlib


def pad_cik(cik: str) -> str:
    """CIK (central index key) needs to be 10 digits (leading zeros) when requesting the submissions JSON."""
    return cik.zfill(10)


def save_html_to_file(html_text: str, path: str) -> None:
    """
    Save HTML text to a file.
    If it already exists, it will be overwritten.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_text)


def convert_html_to_pdf_wkhtml(html_path: str, pdf_path: str) -> bool:
    try:
        # pdfkit configuration - uses system wkhtmltopdf binary
        # If wkhtmltopdf is not found, pdfkit will raise an OSError
        pdfkit.from_file(html_path, pdf_path)
        return True
    except Exception as e:
        print(f"wkhtmltopdf/html->pdf conversion failed: {e}")
        return False


def compute_hash(text: str) -> str:
    """Return a stable SHA256 hash of normalized text."""
    normalized = " ".join(text.split())  # remove extra whitespace/newlines
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


# File operations
def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
