select 
    date_trunc('month', ts) as month,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by month