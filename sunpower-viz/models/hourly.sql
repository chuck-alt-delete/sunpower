select 
    ts,
    year(ts) as year,
    month(ts) as month,
    day(ts) as day,
    production,
    consumption,
    grid
from sunpower