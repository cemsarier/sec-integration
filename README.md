# Installation
To run this project, follow these steps:
* Install `uv` as package manager, follow the steps here https://docs.astral.sh/uv/getting-started/installation/#pypi
* Install wkhtmltopdf by following the instructions at https://wkhtmltopdf.org/downloads.html
* Clone the repository: `git clone https://github.com/cemsarier/sec-integration`
* Navigate to the project directory
* Install the required dependencies with uv: `uv sync`
* Make sure you can run the tests: `uv run pytest` without errors
* Run the application: `uv run python main.py`
* Results will be available in the specified `output` folder. By default, it is set to "sec_10k_output" folder.
* If pdf conversion raises an error on a Windows machine, ensure that the path to wkhtmltopdf is correctly specified in `core/utils.py/convert_html_to_pdf` function.


# Project Structure
* `core/` - contains the main application logic, including modules for fetching filings, processing HTML content, and converting to PDF.
* `tests/` - contains test cases to validate the functionality of the application.
* `main.py` - the entry point of the application.

# Used Tools and Libraries
## Package manager
* `uv` - for managing project dependencies and running scripts.

## Testing
* `pytest` - for writing and running tests to ensure code quality.
* `hashlib` - for generating hash values, useful in testing if the html content has changed.
* `pickle` - for serializing and deserializing Python objects during testing.

## Code quality
* `black` - for code formatting to maintain a consistent style.
* `ruff` - for linting and enforcing coding standards.
* `mypy` - for static type checking to catch type-related errors and potential bugs.

## Main libraries
* `requests` - for making HTTP requests to fetch data from the SEC EDGAR database.
* `pdfkit` - for converting downloaded HTML content to PDF format. It uses wkhtmltopdf as a backend, and this is an external dependency that needs to be installed separately.

# Potential Improvements
* Data quality checks and validation to ensure the integrity of downloaded filings.
* Asynchronous downloading to improve performance when fetching multiple filings.
* Enhanced error handling and logging for better debugging and monitoring.
* Alternatives to pdfkit for HTML to PDF conversion, such as `WeasyPrint` or `reportlab`. This could help avoid the dependency on wkhtmltopdf.