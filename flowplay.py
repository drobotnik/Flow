a = [(0, 1), (2, 4), (3, 3), (10, 20)]
print(a)
a = sorted(a, key=lambda x: x[0] - x[1])
print(a)