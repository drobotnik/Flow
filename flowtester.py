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

t = Level(t2l42)
x = Level(t2l51)
y = Level(t2l52)
z = Level(t2l53)

l = [t, x, y, z]

for level in l:
    print(level)
    # for area in level.area_finder():
    #     print(area)
    print(level.all_areas_shared())
    print('pud', level.dammed())
    print()


