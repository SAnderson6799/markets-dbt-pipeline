select price_date, ticker, count(*) as n
from {{ ref('stg_prices') }}
group by 1, 2
having count(*) > 1
