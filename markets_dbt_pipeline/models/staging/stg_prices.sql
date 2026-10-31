select
    cast(price_date as date) as price_date,
    upper(ticker) as ticker,
    open,
    high,
    low,
    close,
    volume
from {{ ref('raw_prices') }}
