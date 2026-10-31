#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source .venv/bin/activate
python scripts/fetch_prices.py
cd markets_dbt_pipeline
dbt seed
dbt run
dbt test
echo "Refresh complete"
