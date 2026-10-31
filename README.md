# Markets dbt Pipeline

A dbt + DuckDB project that turns Yahoo Finance price data into daily returns, moving averages and volatility.

## Pipeline

    raw_prices (seed) -> stg_prices -> fct_daily_returns -> fct_price_stats

| Model | What it does |
|---|---|
| raw_prices | Daily OHLCV prices fetched with yfinance (loaded as a dbt seed) |
| stg_prices | Cleans types and standardises ticker names |
| fct_daily_returns | Daily return per ticker, from the previous close |
| fct_price_stats | 20-day moving average and 20-day volatility (daily and annualised) |

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install dbt-core dbt-duckdb yfinance pandas

dbt needs a profile named `markets_dbt_pipeline` in its default `profiles.yml` (in `~/.dbt/`), using the DuckDB adapter.

## Run

    python scripts/fetch_prices.py
    cd markets_dbt_pipeline
    dbt seed
    dbt run
    dbt test

Edit the `TICKERS` list in `scripts/fetch_prices.py` to change which prices are pulled.

## Notes

- The DuckDB file is not committed, so run the steps above to rebuild it.
- Prices come from Yahoo Finance through an unofficial API, so treat them as a personal-project data source.
