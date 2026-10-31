select *
from {{ ref('fct_price_stats') }}
where vol_20d < 0
