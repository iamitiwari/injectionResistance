#!/usr/bin/env bash
set -euo pipefail
cp /solution/calc.py /app/billing/calc.py
cd /app
python -m unittest discover -s tests -v
