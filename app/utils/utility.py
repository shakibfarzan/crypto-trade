def condition_AND_list(conditions: list([bool])) -> bool:
  for cond in conditions:
    if not cond:
      return False
  return True

def generate_slug(name: str):
  lst = name.lower().split(' ')
  return '-'.join(lst)