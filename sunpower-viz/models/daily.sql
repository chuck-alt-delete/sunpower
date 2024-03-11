select 
    date_trunc('day', ts) as day,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by day