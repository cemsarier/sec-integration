# Installation
To run this project, follow these steps:
* Install uv as package manager, follow thw steps here https://docs.astral.sh/uv/getting-started/installation/#pypi
* Install wkhtmltopdf:
  * Windows: by following the instructions at https://wkhtmltopdf.org/downloads.html
  * macOS: using Homebrew with the command `brew install wkhtmltopdf`
* Clone the repository: `git clone https://github.com/cemsarier/sec-integration`
* Navigate to the project directory
* Install the required dependencies with uv: `uv sync`
* Run the application: `uv run python main.py`
* If pdf conversion raises an error on a Windowd machine, ensure that the path to wkhtmltopdf is correctly specified in `core/utils.py/convert_html_to_pdf` function.