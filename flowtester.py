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
y = Level(t2l52)



print(t)
print(t.connected_areas())


print(y)
print(y.connected_areas())
