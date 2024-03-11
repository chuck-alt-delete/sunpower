-- create some helpful views
create view sunpower_hourly as
select 
    ts,
    year(ts) as year,
    month(ts) as month,
    day(ts) as day,
    production,
    consumption,
    grid
from sunpower;

create view sunpower_daily as
select 
    date_trunc('day', ts) as day,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by day;

create view sunpower_monthly as
select 
    date_trunc('month', ts) as month,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by month;

create view sunpower_yearly as
select 
    date_trunc('year', ts) as year,
    sum(production) as production,
    sum(consumption) as consumption,
    sum(grid) as grid
from sunpower 
group by year;

-- output aggregates to csvs
copy (select * from sunpower_daily) to './data/aggregates/daily.csv';
copy (select * from sunpower_monthly) to './data/aggregates/monthly.csv';
copy (select * from sunpower_yearly) to './data/aggregates/yearly.csv';

-- daily avg per month
select 
    month(d),
    avg(production) production,
    avg(consumption) consumption,
    avg(grid) grid
from sunpower_daily 
group by month(d) 
order by grid;

