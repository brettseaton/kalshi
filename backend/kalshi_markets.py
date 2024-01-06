# kalshi_markets.py

from KalshiClientsBaseV2 import ExchangeClient
import kalshi_python
import time
from datetime import datetime, timedelta
import json
import requests

def fetch_kalshi_markets(client, days=5, pages=10):
    current_ts = int(time.time())
    future_ts = int((datetime.utcnow() + timedelta(days=days)).timestamp())
    all_markets = []
    cursor = None
    for _ in range(pages):
        market_params = {
            'limit': 100,
            'cursor': cursor,
            'event_ticker': None,
            'series_ticker': None,
            'max_close_ts': future_ts,
            'min_close_ts': current_ts,
            'status': None,
            'tickers': None
        }

        markets_response = client.get_markets(**market_params)
        if isinstance(markets_response, str):
            markets_response = json.loads(markets_response)

        markets = markets_response.get('markets', markets_response) if isinstance(markets_response, dict) else markets_response
        all_markets.extend(markets)

        cursor = markets_response.get('cursor')  # Update the cursor for the next call
        if not cursor:
            break  # Exit the loop if there's no more pages

    return all_markets


def fetch_all_events(base_url):
    all_events = []
    cursor = None
    headers = {"accept": "application/json"}

    while True:
        params = {'limit': 100, 'cursor': cursor}  # None for the first request
        response = requests.get(f"{base_url}/events", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            all_events.extend(data['events'])
            cursor = data.get('cursor')
            if not cursor:  # Check if there's a next page
                break
        else:
            print(f"Failed to fetch events: {response.status_code} - {response.text}")
            break

    return all_events

def filter_dead_markets(markets):
    filtered_markets = []
    for market in markets:
        liquidity = market.get("liquidity")
        volume = market.get("volume")
        if liquidity != 0 and volume != 0:
                filtered_markets.append(market)
    return filtered_markets

def just_titles(markets):
    titles = []
    for market in markets:
        title = market.get("title")
        titles.append(title)
    return titles


def runthis():
    # Replace with your credentials and base URL
    demo_email = "brettseaton0@gmail.com"
    demo_password = "Man-42848"
    demo_api_base = "https://demo-api.kalshi.co/trade-api/v2"

    # Initialize Kalshi Exchange Client
    exchange_client = ExchangeClient(exchange_api_base=demo_api_base, email=demo_email, password=demo_password)
    
    # Fetch and process markets
    markets = fetch_kalshi_markets(exchange_client)
    filtered = filter_dead_markets(markets)
    titles = just_titles(filtered)
    return(titles)
    # print(json.dumps(filtered, indent=4))
    # events_response = fetch_all_events(demo_api_base)
    
    # Process the response as needed
    # print(json.dumps(markets_response, indent=4))
    # print(json.dumps(events_response, indent=4))
