import requests
import pandas as pd
import json
from datetime import datetime

# Constants
API_KEY = "758c2e749d7f42ff838022c0adea1470"  # Replace with your BLS API key
SERIES_IDS = ["CEU0000000001", "LNS14000000","LNS11300000","LNS12300000","LNS12032194"]
# Non-farm workers, unemployment rate,Labor Force Participation Rate,Civilian Employment-Population Ratio,Part-Time for Economic Reasons
START_YEAR = "2022"
END_YEAR = str(datetime.now().year)

def fetch_bls_data(series_ids, start_year, end_year, api_key):
    """Fetch data from BLS API."""
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": api_key
    })
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise ValueError("Error fetching data from BLS API.")
    return response.json()["Results"]["series"]

def process_bls_data(data):
    """Process raw data into a DataFrame."""
    records = []
    for series in data:
        series_id = series["seriesID"]
        for entry in series["data"]:
            records.append({
                "series_id": series_id,
                "year": int(entry["year"]),
                "period": entry["period"],
                "period_name": entry["periodName"],
                "value": float(entry["value"]),
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    data = fetch_bls_data(SERIES_IDS, START_YEAR, END_YEAR, API_KEY)
    df = process_bls_data(data)
    df.to_csv("data/labor_stats.csv", index=False)
    print("Data collection complete.")
