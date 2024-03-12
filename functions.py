import requests
import dotenv
import os
import csv

dotenv.load_dotenv('./.env', override=True)
SITEKEY = os.getenv('site_key')
TOKEN = os.getenv('token')
URL = "https://edp-api-graphql.edp.sunpower.com/graphql"
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")

def get_token():
    """
    TODO: Get jwt using session token.
    This function currently gets the login response from basic username/password login.
    I am as yet unsure how SunPower's OAuth2 flow results in a JSON Web Token (jwt) from this.
    """
    auth_url = "https://login.mysunpower.com/api/v1/authn"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"password": PASSWORD, "username": USERNAME}
    return requests.post(auth_url,headers=headers, json=payload).json()

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Host": "edp-api-graphql.edp.sunpower.com",
    "Origin": "https://sds.mysunpower.com",
    "Referer": "https://sds.mysunpower.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Authorization": f"Bearer {TOKEN}" # TODO: Replace TOKEN with get_token() once the function returns a jwt
}


def get_aggregates(start, end):
    query = {
        "operationName": "EnergyRange",
        "variables": {
            "siteKey": SITEKEY,
            "interval": "hour",
            "end": end,
            "start": start
        },
        "query": """
        query EnergyRange($interval: String!, $end: String!, $start: String!, $siteKey: String!) {
          energyRange(interval: $interval, end: $end, start: $start, siteKey: $siteKey) {
            totalProduction
            totalConsumption
            energyMixPercentage
            totalGridImport
            totalGridExport
            netGridImportExport
          }
        }
        """
    }

    response = requests.post(URL, headers=HEADERS, json=query).json()
    try:
        totals = {key: response["data"]["energyRange"][key] for key in ["totalProduction","totalConsumption","energyMixPercentage","totalGridImport","totalGridExport","netGridImportExport"]}
        return totals
    except Exception:
        print(response)

def get_timeseries(start, end):
    query = {
        "operationName": "EnergyRange",
        "variables": {
            "siteKey": SITEKEY,
            "interval": "hour",
            "end": end,
            "start": start
        },
        "query": """
        query EnergyRange($interval: String!, $end: String!, $start: String!, $siteKey: String!) {
          energyRange(interval: $interval, end: $end, start: $start, siteKey: $siteKey) {
            energyDataSeries {
              consumption
              grid
              production
            }
          }
        }
        """
    }

    response = requests.post(URL, headers=HEADERS, json=query).json()
    if not response["data"]:
        print(response)
        print("You probably need a new token.")
        raise ValueError
    # combine timeseries for production, consumption, and grid
        # get timestamps and populate consumption.
    timeseries = {reading[0]: {"consumption": reading[1]} for reading in response["data"]["energyRange"]["energyDataSeries"]["consumption"]}
    # add production
    for reading in response["data"]["energyRange"]["energyDataSeries"]["production"]:
        timeseries[reading[0]]["production"] = reading[1]
    # add grid
    for reading in response["data"]["energyRange"]["energyDataSeries"]["grid"]:
        timeseries[reading[0]]["grid"] = reading[1]
    # flatten
    final_timeseries = []
    for timestamp in timeseries:
        final_timeseries.append(
            {
            "ts": timestamp.replace('T',' '),
            "consumption": timeseries[timestamp]["consumption"],
            "production": timeseries[timestamp]["production"],
            "grid": timeseries[timestamp]["grid"]
            }
        )
    return final_timeseries

def write_timeseries(path, timeseries):
    with open(path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ts', 'consumption', 'production', 'grid'])
        if os.path.getsize(path) == 0:
            writer.writeheader()
        for row in timeseries:
            writer.writerow(row)


if __name__ == "__main__":
    print(get_aggregates("2024-03-10T00:00:00", "2024-03-10T23:59:59"))
