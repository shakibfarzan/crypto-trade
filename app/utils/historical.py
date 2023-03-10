from app.models import Historical
from app.utils.utility import condition_AND_list, generate_slug, get_diff_percent

def convert_historical_query(queryset: list([Historical]), price, volume, dominance):
  map = {}
  for item in queryset:
    map[item.symbol] = {
      "Name": item.name,
      "Symbol": item.symbol,
      "Price": get_diff_percent(map[item.symbol]["Price"], float(item.price)) if item.symbol in map else float(item.price),
      "Volume": get_diff_percent(map[item.symbol]["Volume"], float(item.volume)) if item.symbol in map else float(item.volume),
      "Dominance": get_diff_percent(map[item.symbol]["Dominance"], float(item.dominance)) if item.symbol in map else float(item.dominance),
      "Volume / Market cap": get_diff_percent(map[item.symbol]["Volume / Market cap"], float(item.volume_divided_market)) if item.symbol in map else float(item.volume_divided_market),
      "slug": generate_slug(item.name)
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