import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import environ

from trade.settings import BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': env("API_KEY"),
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

def condition_AND_list(conditions: list([bool])) -> bool:
  for cond in conditions:
    if not cond:
      return False
  return True

def filter_data(data, search, vol_change_min, dom_min, vol_per_mcap_min):
  filtered_data = []
  for item in data:
    conditions = []
    if search:
      conditions.append(search in item["Name"])
    if vol_change_min != None:
      conditions.append(float(vol_change_min) <= item["Volume change 24h"])
    if dom_min != None:
      conditions.append(float(dom_min) <= item["Market cap dominance"])
    if vol_per_mcap_min != None:
      conditions.append(float(vol_per_mcap_min) <= item["Volume 24h / market cap"])
    if condition_AND_list(conditions):
      filtered_data.append(item)
  return filtered_data

def get_watchlist(search, vol_change_min, dom_min, vol_per_mcap_min):
  try:
    # parameters = {
    #   'limit', limit,
    #   'start', start,
    # }
    response = session.get(API_URL)
    data = json.loads(response.text)
    return filter_data(formatted_data(data["data"]), search, vol_change_min, dom_min, vol_per_mcap_min)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    return None