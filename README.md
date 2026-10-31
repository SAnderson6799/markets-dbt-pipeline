# Markets Data Pipeline (dbt + DuckDB)

An end-to-end analytics engineering project. It pulls daily prices from Yahoo Finance, transforms them with dbt, tests them, and refreshes automatically in the cloud on a weekday schedule.

## What it demonstrates

- **SQL:** window functions (lag for returns, rolling 20-day average and volatility) with partial windows handled explicitly
- **dbt:** layered project (seed, staging, marts), `ref()` lineage, schema tests, singular tests, generated docs
- **Python:** ingestion script using yfinance and pandas
- **Automation:** GitHub Actions workflow that fetches, builds, tests and commits refreshed data each weekday

## Pipeline

    raw_prices (seed) -> stg_prices -> fct_daily_returns -> fct_price_stats

| Model | Grain | Purpose |
|---|---|---|
| raw_prices | ticker, day | Daily OHLCV prices from Yahoo Finance |
| stg_prices | ticker, day | Casts types, standardises ticker names |
| fct_daily_returns | ticker, day | Previous close and simple daily return |
| fct_price_stats | ticker, day | 20-day moving average, 20-day volatility (daily and annualised) |

## Data quality

- Not-null tests on keys in staging and marts
- Singular tests that the ticker + date grain is unique and that volatility is never negative
- Rolling metrics are null until a full 20-day window exists, so early rows never show a misleading average

## Design decisions

- **Seed for ingestion:** keeps the project reproducible with no infrastructure. In production I would load raw data into the warehouse, declare it as a dbt source and add freshness checks.
- **Views for models:** the data is small. At scale I would materialise marts as tables and make the large ones incremental.
- **DuckDB:** zero setup, and the SQL patterns carry over to cloud warehouses with minor dialect changes.
- **Annualised volatility:** daily standard deviation multiplied by the square root of 252 trading days.

## Run it

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ./refresh.sh

`refresh.sh` fetches prices, then runs `dbt seed`, `dbt run` and `dbt test`. Edit the `TICKERS` list in `scripts/fetch_prices.py` to change the instruments. The dbt profile name is `markets_dbt_pipeline` (DuckDB); the cloud run uses `ci/profiles.yml`.

## Limitations and next steps

- Yahoo Finance is an unofficial source, fine for a personal project but not production
- Next: a dashboard (Looker Studio or Tableau Public), correlation between tickers, source freshness checks
