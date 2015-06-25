a = [1, 2, 3]
b = [3, 4, 5]

from itertools import product

for x, y in product(a, b):
    print(x, y)
    if x == y:
        break


def a():
    print('a')
    return False


def b():
    print('b')
    return True


def c():
    print('c')
    return False


def tests():
    yield a()
    yield b()
    yield c()

if any(tests()):
    print('one')