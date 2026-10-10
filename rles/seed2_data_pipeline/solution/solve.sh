#!/usr/bin/env bash
set -euo pipefail
cp /solution/pipeline.py /app/pipeline.py
cd /app
python pipeline.py --input transactions.csv --output report.json
python -m unittest discover -s tests -v
