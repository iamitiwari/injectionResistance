#!/usr/bin/env bash
set -euo pipefail

cd /app

python -m pip install --no-cache-dir -r requirements.txt

python -m pytest tests/ -q  