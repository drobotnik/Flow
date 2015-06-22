from flowlevels import *
from flowmethods import *
from flowRun import *


lt41 = [['1', '1', '', ''],
        ['2', '2', '', ''],
        ['', '', '', ''],
        ['', '', '', '']]



two_flows_blank = [[[], []],
                   [[], []]]

one_flow_blank = [[[], []]]

two_flows = [[[(0, 0), (1, 0)], [(3, 0)]],
             [[(0, 1)], [(0, 2)]]]

one_flows = [[[(1, 0)], [(1, 1)]]]


solve(Level(make_flows(two_flows), 4))