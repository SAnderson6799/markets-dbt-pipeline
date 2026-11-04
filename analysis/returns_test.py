from pathlib import Path
import duckdb
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "markets_dbt_pipeline" / "dev.duckdb"

con = duckdb.connect(str(DB), read_only=True)
df = con.execute("""
    SELECT ticker, price_date, daily_return,
           LAG(daily_return) OVER (PARTITION BY ticker ORDER BY price_date) AS prev_return
    FROM fct_price_stats
""").df().dropna()

rng = np.random.default_rng(42)
rows = []
for ticker, g in df.groupby("ticker"):
    a = g.loc[g.prev_return < 0, "daily_return"].to_numpy()   # after a down day
    b = g.loc[g.prev_return >= 0, "daily_return"].to_numpy()  # after an up day
    diff = a.mean() - b.mean()
    _, p_welch = stats.ttest_ind(a, b, equal_var=False)
    _, p_mw = stats.mannwhitneyu(a, b)
    boots = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(5000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    rows.append({
        "ticker": ticker, "n_after_down": len(a), "n_after_up": len(b),
        "mean_diff": diff, "ci_low": lo, "ci_high": hi,
        "cohens_d": diff / pooled, "p_welch": p_welch, "p_mannwhitney": p_mw,
    })

res = pd.DataFrame(rows)
res["p_welch_bonferroni"] = (res.p_welch * len(res)).clip(upper=1)
res.to_csv(ROOT / "analysis" / "returns_test_results.csv", index=False)
print(res.round(4).to_string(index=False))
