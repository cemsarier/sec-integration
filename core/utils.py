"""Contains utility functions for the project."""

import os
import sys
import pdfkit
import hashlib
from typing import Optional


def pad_cik(cik: str) -> str:
    """CIK (central index key) needs to be 10 digits (leading zeros) when requesting the submissions JSON."""
    return cik.zfill(10)


def save_html_to_file(html_text: str, path: str) -> None:
    """
    Save HTML text to a file.
    If it already exists, it will be overwritten.
    """
    create_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_text)


def convert_html_to_pdf(html_path: str) -> Optional[str]:
    # On Windows, specify the path to wkhtmltopdf executable
    if sys.platform.startswith("win"):
        config = pdfkit.configuration(
            wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        )
    else:
        config = None
    output_path = html_path.replace(".html", ".pdf")

    try:
        # pdfkit configuration - uses system wkhtmltopdf binary
        # If wkhtmltopdf is not found, pdfkit will raise an OSError
        pdfkit.from_file(
            html_path,
            output_path,
            configuration=config,
            options={"enable-local-file-access": ""},
        )
        print(f"Converted HTML to PDF: {output_path}")
        return output_path
    except Exception as e:
        print(f"wkhtmltopdf/html->pdf conversion failed: {e}")
        return None


def compute_hash(text: str) -> str:
    """Return a stable SHA256 hash of normalized text."""
    normalized = " ".join(text.split())  # remove extra whitespace/newlines
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


# File operations
def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
