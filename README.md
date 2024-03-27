```markdown
# PyScript

PyScript is a Python-based tool designed to automate the extraction of JavaScript files and API endpoints from web applications. It can recursively scan a website or a list of websites, download JavaScript files, and identify potential API endpoints within them.

## Features

- **Website Crawling:** Recursively visits all accessible pages within a domain.
- **JavaScript Extraction:** Identifies and lists all JavaScript files used in the web application.
- **Endpoint Detection:** Extracts potential API endpoints from the JavaScript files.
- **File Downloading:** Optionally downloads all discovered JavaScript files for offline analysis.

## Prerequisites

Before you start using PyScript, make sure you have the following installed:
- Python 3.x
- `requests` library
- `BeautifulSoup4` library

You can install the necessary Python libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Installation

1. Clone the repository or download the source code.
2. Ensure you have the prerequisites installed.
3. Navigate to the PyScript directory.

## Usage

To use PyScript, you can run it from the command line, providing the necessary arguments.

```bash
python pyscript.py [options] <URL or file>
```

### Options

- `--download`: Download all discovered JavaScript files to the local system.
- `--find-endpoints`: Extract and list all potential API endpoints from the JavaScript files.

### Examples

- Scan a single website and list JavaScript files:

  ```bash
  python pyscript.py http://example.com
  ```

- Scan a website, download JavaScript files, and extract endpoints:

  ```bash
  python pyscript.py --download --find-endpoints http://example.com
  ```

- Scan multiple websites from a file:

  ```bash
  python pyscript.py --find-endpoints urls.txt
  ```

## Contributing

Contributions to PyScript are welcome! If you have suggestions for improvements or encounter any issues, please feel free to submit an issue or pull request.

