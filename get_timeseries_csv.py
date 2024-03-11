from functions import write_timeseries
from functions import get_timeseries

if __name__ == "__main__":
    write_timeseries(
        './data/timeseries/sunpower_timeseries.csv',
        get_timeseries("2024-03-10T00:00:00", "2024-03-10T23:59:59")
    )