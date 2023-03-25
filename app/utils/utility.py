def condition_AND_list(conditions: list([bool])) -> bool:
  for cond in conditions:
    if not cond:
      return False
  return True

def generate_slug(name: str):
  lst = name.lower().split(' ')
  return '-'.join(lst)

def get_diff_percent(first_arg, second_arg):
  try:
    diff_percent = ((second_arg - first_arg) * 100) / first_arg
    return round(diff_percent,3)
  except (KeyError, ZeroDivisionError) as e:
    return 0