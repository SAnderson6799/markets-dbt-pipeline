select price_date, ticker, count(*) as n
from {{ ref('fct_price_stats') }}
group by 1, 2
having count(*) > 1
