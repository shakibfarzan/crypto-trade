import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import environ
from app.utils.utility import condition_AND_list, generate_slug

from trade.settings import BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CMC_CURRENCY_URL = "https://coinmarketcap.com/currencies"
CMC_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

CMC_headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': env("CMC_API_KEY"),
}

session = Session()


def formatted_data(data):
  formatted_data = []
  for item in data:
    usd_quote = item["quote"]["USD"]
    name = item["name"]
    symbol = item["symbol"]
    price = usd_quote["price"]
    volume_24h = usd_quote["volume_24h"]
    volume_change_24h = usd_quote["volume_change_24h"]
    market_cap = usd_quote["market_cap"]
    market_cap_dominance = usd_quote["market_cap_dominance"]
    volume_24h_per_market_cap = 0
    if market_cap > 0:
      volume_24h_per_market_cap = volume_24h / market_cap
    dict = { 
            "Name": name,
            "Symbol": symbol,
            "Price": round(price, 3), 
            "Volume 24h": round(volume_24h, 3),
            "Volume change 24h": round(volume_change_24h, 3),
            "Market cap": round(volume_change_24h, 3),
            "Market cap dominance": round(market_cap_dominance, 3),
            "Volume 24h / market cap": round(volume_24h_per_market_cap, 3),
            "slug": generate_slug(name)
        }
    formatted_data.append(dict)
  return formatted_data

def filter_data(data, search, vol_change_min, dom_min, vol_per_mcap_min):
  filtered_data = []
  for item in data:
    conditions = []
    if search:
      conditions.append(search in item["Name"])
    if vol_change_min != None and vol_change_min != '':
      conditions.append(float(vol_change_min) <= item["Volume change 24h"])
    if dom_min != None and dom_min != '':
      conditions.append(float(dom_min) <= item["Market cap dominance"])
    if vol_per_mcap_min != None and vol_per_mcap_min != '':
      conditions.append(float(vol_per_mcap_min) <= item["Volume 24h / market cap"])
    if condition_AND_list(conditions):
      filtered_data.append(item)
  return filtered_data

def get_watchlist(search, vol_change_min, dom_min, vol_per_mcap_min, page, page_size):
  start = ((int(page) - 1) * int(page_size) + 1)
  try:
    parameters = {
      'limit': page_size,
      'start': start,
    } 
    session.headers.update(CMC_headers)
    response = session.get(CMC_API_URL, params=parameters)
    data = json.loads(response.text)
    return data["status"]["total_count"], filter_data(formatted_data(data["data"]), search, vol_change_min, dom_min, vol_per_mcap_min)
  except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
    return None
  