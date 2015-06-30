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

l = [[n, Level(x)] for n, x in enumerate([t1l31, t1l32, t1l33, t1l34, t1l35,  # 32 and 33 should be false (0, 2) is blocked
                                          t2l31,
                                          t2l41, t2l42, t2l43, t2l44,
                                          t2l51, t2l52, t2l53, t2l54])]

# t2l31 - needs to throw a trigger somewhere along the way
# t2l54 - How do I handle this? Maybe Flow ends count as being in two areas if possible.
# In this case, B will be blocked whichever way A moves.
# This should be coming up as False somewhere.

# t2l44 - How do I handle this?. Need to check both pairs are in an area

for n, level in l:
    print(n)
    print(level)
    # print(len(level.ends()) == len(level), level.size ** 2 == len(level.filled()) + len(level.empties()))
    if False: # not any([level.blocked(), level.dammed(), level.separated_flows(), level.cornered(), True]):
        print('OK')
    else:
        tests = [['Dammed areas', level.dammed()],
                 ['Flows seperated', level.separated_flows()],
                 ['Blocked flows', level.blocked()],
                 ['Cornered', level.cornered()],
                 ['Folded', level.folded()]]
        for name, test in tests:
            if name == 'Folded':
            #if test:
                print(name, test)
    # area_finder = level.area_finder()
    # print('Number of areas: {}'.format(len(area_finder)))
    # for na, area in enumerate(area_finder):
    # print("Area {}: {}".format(na, area))
    print()

