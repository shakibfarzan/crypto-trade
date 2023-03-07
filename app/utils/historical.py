from app.models import Historical
from app.utils.utility import condition_AND_list

def convert_historical_query(queryset: list([Historical]), price, volume, dominance):
  map = {}
  for item in queryset:
    map[item.symbol] = {
      "Symbol": item.symbol,
      "Name": item.name,
      "Price": map[item.symbol]["Price"] - float(item.price) if item.symbol in map else float(item.price),
      "Volume": map[item.symbol]["Volume"] - float(item.volume) if item.symbol in map else float(item.volume),
      "Dominance": map[item.symbol]["Dominance"] - float(item.dominance) if item.symbol in map else float(item.dominance)
    }
  all = list(map.values())
  filtered_data = []
  for item in all:
    conditions = []
    if price != None and price != '':
      conditions.append(float(price) <= item["Price"])
    if volume != None and volume != '':
      conditions.append(float(volume) <= item["Volume"])
    if dominance != None and dominance != '':
      conditions.append(float(dominance) <= item["Dominance"])
    if condition_AND_list(conditions):
      filtered_data.append(item)
  return filtered_data