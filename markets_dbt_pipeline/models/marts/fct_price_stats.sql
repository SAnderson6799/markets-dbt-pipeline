select
    price_date,
    ticker,
    close,
    daily_return,
    case when count(close) over w = 20
         then avg(close) over w end as ma_20,
    case when count(daily_return) over w = 20
         then stddev_samp(daily_return) over w end as vol_20d,
    case when count(daily_return) over w = 20
         then stddev_samp(daily_return) over w * sqrt(252) end as vol_20d_annualised
from {{ ref('fct_daily_returns') }}
window w as (
    partition by ticker
    order by price_date
    rows between 19 preceding and current row
)
