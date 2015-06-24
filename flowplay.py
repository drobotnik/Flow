a = [1, 2, 3]
b = [3, 4, 5]

from itertools import product

for x, y in product(a, b):
    print(x, y)
    if x == y:
        break