select 
    date_trunc('year', ts) as year,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by year