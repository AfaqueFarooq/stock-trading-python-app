
import requests
import os
from dotenv import load_dotenv
import time
import csv

load_dotenv()

MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")

LIMIT = 1000
url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={MASSIVE_API_KEY}'

# schema
FIELDS = {
    "ticker": "",
    "name": "",
    "market": "",
    "locale": "",
    "primary_exchange": "",
    "type": "",
    "active": "",
    "currency_name": "",
    "cik": "",
    "composite_figi": "",
    "share_class_figi": "",
    "last_updated_utc": "",
}

fieldnames = list(FIELDS.keys())
csv_file = "tickers.csv"

# first request
response = requests.get(url)
tickers = []

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

# pagination
while 'next_url' in data:
    print('requesting next page',data['next_url'])
    time.sleep(12)  # To respect rate limits as we using free tier of Massive API
    response = requests.get(
        data['next_url'] + f'&apiKey={MASSIVE_API_KEY}'
        )
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)

# write tickers to CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for t in tickers:
        row = {key: t.get(key, "") for key in fieldnames}
        writer.writerow(row)

print(f"Wrote {len(tickers)} rows to {csv_file}")