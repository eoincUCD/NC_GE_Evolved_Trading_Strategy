def p():
  x = 0.0
  for i in range(5+1):
    for i in range(6+1):
      for i in range(6+1):
        x = (x + 0.5)
        x = (x + 0.5)
    for i in [0, 4, 5, 3]:
      for i in range(5+1):
        x = (x + 0.5)
    x = (x + 0.5)
  for i in [0]:
    x = (x + 0.5)
  return x

if __name__ == "__main__":
  print(p())