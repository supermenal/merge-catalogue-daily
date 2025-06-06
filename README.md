# merge-catalogue-daily

This repo will contain:

- `merge_catalogues.py`: the Python script that fetches UK/FR CSVs, merges them, and tags each row.
- `.github/workflows/daily.yml`: a GitHub Actions workflow that (each morning) runs `merge_catalogues.py` and pushes `combined.csv` back into `main`.
- `combined.csv`: the merged file (automatic).
