# url-explorer

url-explorer scans a folder and its subfolders for HTTP and HTTPS URLs. It prints every URL together with the file where it was found, followed by a count of the URLs found in that file.

You can optionally limit the scan to one website and export the results to an Excel workbook for sorting and further analysis.

## Installation

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Basic usage

Scan the current folder:

```bash
python url-explorer.py .
```

Scan a specific folder:

```bash
python url-explorer.py /path/to/folder
```

## Filter by website

Use `--base-url` to find URLs from a specific scheme and host. Paths below that host are included:

```bash
python url-explorer.py . --base-url https://example.com
```

## Export to Excel

Use `--export-excel` to save the results as an `.xlsx` file while still printing them to the terminal:

```bash
python url-explorer.py . --export-excel url-results.xlsx
```

The workbook contains one row for each found URL with these columns:

- `file`: the file containing the URL
- `url`: the URL that was found
- `url_count`: the total number of matching URLs in that file

Options can be combined:

```bash
python url-explorer.py . \
	--base-url https://example.com \
	--export-excel example-results.xlsx
```

## Ignoring files and folders

Create a `fileignore.txt` file in the folder being scanned to skip files and folders. Add one file or folder name, or a relative path, per line. Empty lines and lines beginning with `#` are ignored.

Example `fileignore.txt`:

```text
venv
node_modules
archive/old-files
README.md
```

The script skips `fileignore.txt` itself and does not scan the Python script that is currently running.
