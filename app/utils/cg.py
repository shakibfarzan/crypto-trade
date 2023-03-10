import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import environ

from trade.settings import BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CG_API_URL = 'https://open-api.coinglass.com/public/v2/open_interest'

CG_headers = {
    "accept": "application/json",
    "coinglassSecret": env("CG_API_KEY"),
}

session = Session()

def formatted_OI(data):
  dict = {
    "Open Interest": round(data["openInterest"], 3),
    "1 hour OI change %": round(data["h1OIChangePercent"], 3),
    "4 hours OI change %": round(data["h4OIChangePercent"], 3),
    "24 hours OI change %": round(data["h24Change"], 3),
    "OI amount": round(data["openInterestAmount"], 3),
    "Volume": round(data["volUsd"], 3),
    "Volume change %": round(data["volChangePercent"], 3),
    "Average funding rate": round(data["avgFundingRate"], 3),
  }
  return dict

def get_oi(symbol):
  try:
    paramteres = {
      'symbol': symbol
    }
    session.headers.update(CG_headers)
    response = session.get(CG_API_URL, params=paramteres)
    data = json.loads(response.text)
    oi_all_data = None
    for item in data["data"]:
      if item["exchangeName"] == "All":
        oi_all_data = item
        break
    return formatted_OI(oi_all_data)
  except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
    return None
  