a = (3, 3, 3)
b = (1, 3)

from itertools import product

for c, r in product(range(2), repeat=2):
    print(c, r)