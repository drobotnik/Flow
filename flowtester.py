from flowlevels import *
from flowmethods import *
from flowRun import *
from testlevels import *
from itertools import product


lt41 = [['1', '', '', '1'],
        ['2', '', '', '2'],
        ['3', '', '', '3'],
        ['4', '', '', '4']]

two_flows_blank = [[[], []],
                   [[], []]]

one_flow_blank = [[[], []]]

t = Level(t2l41)

print(t)

filled = []
for flow in t:
    filled += flow.path

empties = []
for spot in product(range(t.size), repeat=2):
    if spot not in filled:
        empties += [spot]

areas = []
while empties:
    area = [empties.pop()]
    for spot in area:
        # print(spot, t.find_adjacent(spot))
        for adj in t.find_adjacent(spot):
            if adj in empties:
                area += [empties.pop(empties.index(adj))]
    areas += [area]

print(areas)
print(empties)


# base = [['', '', ''],
#         ['', '', ''],
#         ['', '', '']]
#
# for r, row in enumerate(base):
#     for c, col in enumerate(row):
#         print((r, c))
#
