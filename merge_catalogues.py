#!/usr/bin/env python3
import requests
import csv
import io
import sys
from datetime import datetime

def fetch_csv_text(url, timeout=30):
    """Download the CSV at `url` and return its content as a UTF-8 string."""
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text

def merge_two_csvs(uk_url, fr_url, out_path):
    """Fetch UK+FR CSVs, drop any malformed rows, tag rows, and write a merged CSV."""
    # 1. Download raw CSV text
    uk_text = fetch_csv_text(uk_url)
    fr_text = fetch_csv_text(fr_url)

    # 2. Wrap in StringIO for csv.reader
    uk_buf = io.StringIO(uk_text)
    fr_buf = io.StringIO(fr_text)

    reader_uk = csv.reader(uk_buf, delimiter=';')
    reader_fr = csv.reader(fr_buf, delimiter=';')

    # 3. Read and build headers
    uk_header = next(reader_uk, [])
    next(reader_fr, None)  # skip FR header
    combined_header = uk_header + ["product_type"]

    # How many columns each input row must have
    expected_cols = len(uk_header)

    # 4. Open output file and write header
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout, delimiter=';')
        writer.writerow(combined_header)

        # Helper to process one CSV reader
        def process(reader, tag):
            for lineno, row in enumerate(reader, start=2):
                # Skip rows that don't match the header width
                if len(row) != expected_cols:
                    print(f"WARNING: skipping malformed row {lineno} in {tag} (got {len(row)} cols, expected {expected_cols})")
                    continue
                # Write the clean row + our product_type tag
                writer.writerow(row + [tag])

        # 5. Process both UK and FR
        process(reader_uk, "UK")
        process(reader_fr, "FR")

    print(f"SUCCESS: wrote merged CSV to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: merge_catalogues.py <UK_URL> <FR_URL> <OUTPUT_PATH>")
        sys.exit(1)

    uk_url   = sys.argv[1]
    fr_url   = sys.argv[2]
    out_path = sys.argv[3]
    merge_two_csvs(uk_url, fr_url, out_path)
