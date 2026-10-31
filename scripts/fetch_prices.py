import yfinance as yf
import pandas as pd

TICKERS = ["AAPL", "MSFT", "SPY"]

frames = []
for t in TICKERS:
    df = yf.Ticker(t).history(period="2y", auto_adjust=True).reset_index()
    df["ticker"] = t
    frames.append(df)

out = pd.concat(frames)
out["price_date"] = pd.to_datetime(out["Date"]).dt.date
out = out.rename(columns={
    "Open": "open", "High": "high", "Low": "low",
    "Close": "close", "Volume": "volume",
})
out = out[["price_date", "ticker", "open", "high", "low", "close", "volume"]]
out.to_csv("markets_dbt_pipeline/seeds/raw_prices.csv", index=False)
print(f"Wrote {len(out)} rows")
