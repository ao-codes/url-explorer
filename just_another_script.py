"""Print URLs found in files below a directory."""

import argparse
import os
import re
from pathlib import Path
from urllib.parse import urlparse


# Match HTTP and HTTPS URLs while stopping at common surrounding punctuation.
URL_PATTERN = re.compile(r"https?://[^\s<>()\[\]{}\"']+")


def base_url_matches(url: str, base_url: str | None) -> bool:
	"""Return whether URL belongs to the requested scheme and host."""
	if base_url is None:
		return True

	# Compare the scheme and host, allowing any path below the base URL.
	url_parts = urlparse(url)
	base_parts = urlparse(base_url)
	return (
		url_parts.scheme.lower() == base_parts.scheme.lower()
		and url_parts.netloc.lower() == base_parts.netloc.lower()
	)


def read_ignored_subfolders(folder: Path) -> set[str]:
	"""Read ignored folder names and relative paths from subignore.txt."""
	ignore_file = folder / "subignore.txt"
	if not ignore_file.is_file():
		return set()

	try:
		# Empty lines and comments are ignored; backslashes become portable separators.
		return {
			line.strip().replace("\\", "/").rstrip("/")
			for line in ignore_file.read_text(encoding="utf-8").splitlines()
			if line.strip() and not line.lstrip().startswith("#")
		}
	except (OSError, UnicodeDecodeError):
		return set()


def find_urls(folder: Path, base_url: str | None = None):
	"""Yield each readable file and its matching URLs."""
	ignored_subfolders = read_ignored_subfolders(folder)
	script_path = Path(__file__).resolve()
	for current_folder, subfolders, filenames in os.walk(folder):
		current_path = Path(current_folder)
		# Mutating this list prevents os.walk from entering ignored directories.
		subfolders[:] = [
			subfolder
			for subfolder in subfolders
			if subfolder not in ignored_subfolders
			and str((current_path / subfolder).relative_to(folder)).replace("\\", "/")
				not in ignored_subfolders
		]

		for filename in sorted(filenames):
			file_path = current_path / filename
			# Never scan the running script or any subignore configuration file.
			if filename == "subignore.txt" or file_path.resolve() == script_path:
				continue
			try:
				contents = file_path.read_text(encoding="utf-8")
			except (OSError, UnicodeDecodeError):
				continue

			urls = []
			for match in URL_PATTERN.finditer(contents):
				url = match.group(0).rstrip(".,;:!?)]}")
				if base_url_matches(url, base_url):
					urls.append(url)
			# Yield the complete list so the caller can print its per-file total.
			yield file_path, urls


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Recursively print URLs found in files."
	)
	parser.add_argument("folder", type=Path, help="Folder to scan")
	parser.add_argument(
		"--base-url",
		help="Only print URLs with this scheme and host, for example https://example.com",
	)
	args = parser.parse_args()

	if not args.folder.is_dir():
		parser.error(f"not a folder: {args.folder}")

	for file_path, urls in find_urls(args.folder, args.base_url):
		# Print each matching URL, followed by the count for this file.
		for url in urls:
			print(f"{file_path}: {url}")
		print(f"{file_path}: {len(urls)} URL(s)")


if __name__ == "__main__":
	main()
