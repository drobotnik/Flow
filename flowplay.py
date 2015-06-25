a = [1, 2, 3]
b = [3, 4, 5]

from itertools import product, chain
from copy import deepcopy, copy

for x, y in product(a, b):
    print(x, y)
    if x == y:
        break


x = chain(*[a, b, [3, 4]])
print(list(x))
for y in copy(x):
    if y == 3:
        print(y)
print(list(x))

for y in copy(x):
    if y == 2:
        print(y)

