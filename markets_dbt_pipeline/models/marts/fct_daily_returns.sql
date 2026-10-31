with prices as (
    select * from {{ ref('stg_prices') }}
)

select
    price_date,
    ticker,
    close,
    lag(close) over (partition by ticker order by price_date) as prev_close,
    close / lag(close) over (partition by ticker order by price_date) - 1 as daily_return
from prices
