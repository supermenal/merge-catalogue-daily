#!/usr/bin/env python3
import requests, csv, io, os
from datetime import datetime

def fetch_csv_text(url, timeout=30):
    """Download the CSV at `url` and return its content as a UTF-8 string."""
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text

def merge_two_csvs(uk_url, fr_url, out_path):
    """Fetch UK+FR CSVs, tag rows, and write a merged CSV to out_path."""
    uk_text = fetch_csv_text(uk_url)
    fr_text = fetch_csv_text(fr_url)

    uk_buf = io.StringIO(uk_text)
    fr_buf = io.StringIO(fr_text)

    reader_uk = csv.reader(uk_buf, delimiter=';')
    reader_fr = csv.reader(fr_buf, delimiter=';')

    # Read UK header (if present)
    uk_header = next(reader_uk, [])
    # Skip FR header (if present)
    next(reader_fr, None)

    # Build combined header
    combined_header = uk_header + ["product_type"]

    # Write merged CSV
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout, delimiter=';')
        writer.writerow(combined_header)

        for row in reader_uk:
            writer.writerow(row + ["UK"])
        for row in reader_fr:
            writer.writerow(row + ["FR"])

    print(f"SUCCESS: wrote merged CSV to {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: merge_catalogues.py <UK_URL> <FR_URL> <OUTPUT_PATH>")
        sys.exit(1)

    uk_url   = sys.argv[1]
    fr_url   = sys.argv[2]
    out_path = sys.argv[3]
    merge_two_csvs(uk_url, fr_url, out_path)

