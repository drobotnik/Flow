from flowlevels import *
from flowmethods import *
from flowRun import *


lt41 = [['', '', '', ''],
        ['2', '2', '', ''],
        ['', '', '', ''],
        ['', '', '', '']]

two_flows_blank = [[[], []],
                   [[], []]]

one_flow_blank = [[[], []]]

two_flows = [[[(0, 0)], [(3, 0)]],
             [[(0, 1)], [(0, 2)]]]

one_flows = [[[(1, 0)], [(1, 1)]]]

lvl = make_level(one_flows, 4)

area = (lvl.size ** 2)
flowspace = 0
areas = []
for flow in lvl:
    flowspace += len(flow.path)
print(flowspace / area)



class NegaFinder(Level):

    def __init__(self, level_obj):
        Level.__init__(self, level_obj)



a = NegaFinder(lt41)

print(a)