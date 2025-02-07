import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL = "https://min-api.cryptocompare.com/data"

def fetch_minute_data(symbol, currency, limit=2000):
    """
    Fetch minute-level historical data from CryptoCompare.
    """
    url = f"{BASE_URL}/v2/histominute"
    params = {
        "fsym": symbol,
        "tsym": currency,
        "limit": limit,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200 or 'Data' not in data:
        raise ValueError(f"Unexpected API response: {data}")
    
    df = pd.DataFrame(data['Data']['Data'])
    if df.empty:
        raise ValueError("No data retrieved from the API.")
    
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def fetch_all_data(symbol, currency, total_points, interval="minute"):
    """
    Fetch historical minute data in batches for larger datasets.
    """
    all_data = []
    limit = 2000
    points_fetched = 0
    to_timestamp = None

    while points_fetched < total_points:
        print(f"Fetching {limit} points...")
        data = fetch_minute_data(symbol=symbol, currency=currency, limit=limit)
        if to_timestamp:
            data = data[data.index < to_timestamp]  # Filter by timestamp to avoid overlaps
        
        if data.empty:
            print("No more data available.")
            break
        
        all_data.append(data)
        points_fetched += len(data)
        to_timestamp = data.index.min()  # Prepare for next batch
        
        print(f"Fetched {len(data)} points. Total so far: {points_fetched}/{total_points}")
    
    return pd.concat(all_data).sort_index()

