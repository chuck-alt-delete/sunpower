select * from sunpower
where date_trunc('day',ts) = '2024-03-10'
order by ts