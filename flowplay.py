from itertools import product
a = [[0, 1, 2],
     [3, 4, 5],
     [6, 7, 8]]

def adj(self, pos):
    row, col = pos
    out = []
    for r, c in product(range(-1, 2), repeat=2):
        if all(0<= index < len(self) for index in (row + r, col + c)):
            out += [(row + r, col + c)]
    return out

print(adj(a, (0, 0)))