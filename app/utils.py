from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '028fd28d-1ee4-410e-88b8-55b0c7e729d9',
}

session = Session()
session.headers.update(headers)

def formatted_data(data):
  formatted_data = []
  for item in data:
    usd_quote = item["quote"]["USD"]
    name = item["name"]
    price = usd_quote["price"]
    volume_24h = usd_quote["volume_24h"]
    volume_change_24h = usd_quote["volume_change_24h"]
    market_cap = usd_quote["market_cap"]
    market_cap_dominance = usd_quote["market_cap_dominance"]
    volume_24h_per_market_cap = volume_24h / market_cap
    dict = { 
            "Name": name, 
            "Price": price, 
            "Volume 24h": volume_24h,
            "Volume change 24h": volume_change_24h,
            "Market cap": market_cap,
            "Market cap dominance": market_cap_dominance,
            "Volume 24h / market cap": volume_24h_per_market_cap
        }
    formatted_data.append(dict)
  return formatted_data

def filter_data(data, search):
  filtered_data = []
  if search:
    for item in data:
      if search in item["Name"]:
        filtered_data.append(item)
    return filtered_data
  return data

def get_watchlist(search):
  try:
    response = session.get(API_URL)
    data = json.loads(response.text)
    return filter_data(formatted_data(data["data"]), search)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    return None