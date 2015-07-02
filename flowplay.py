a = (3, 3, 3)
b = (1, 3, 4, 5, 4, 4, 5, 6)

c = {(0, 1): []}

for n in b:
    c[(0, 1)] += [n]

c['b'] = [3, 4]


new = c.items()

x = ([key, c[key]] for key in c)
y = [[key, c[key]] for key in c]


def test():
    out = []
    for key in c:
        if len(c[key]) == 1:
            return [c[key][0], key]
        else:
            out += [[key, c[key]]]
    return out


print(test())


