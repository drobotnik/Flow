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

l = [[n, Level(x)] for n, x in enumerate([t1l31,
                                          t2l41, t2l42, t2l43, t2l44,
                                          t2l51, t2l52, t2l53, t2l54])]

# t2l54 - How do I handle this? Maybe Flow ends count as being in two areas if possible.
# In this case, B will be blocked whichever way A moves.
# This should be coming up as False somewhere.

# t2l44 - How do I handle this?. Need to check both pairs are in an area

for n, level in l:
    print(n)
    print(level)
    print('Number of areas: {}'.format(len(level.area_finder())))
    print('dammed areas?', level.dammed())
    print('all flow ends share areas?', level.all_areas_shared())
    print('blocked flows?', level.blocked())
    print()


