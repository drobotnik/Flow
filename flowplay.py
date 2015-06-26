
a = [4, 4, 3]
b = [10, 2]
c = [4, 5, 1]

d = [a, b, c]

print(d)

for flow in d:
    flow.sort()

d.sort(key=lambda x: len(x))

print(d)