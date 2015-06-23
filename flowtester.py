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


def area_finder(level_obj):
    filled = []
    for flow in level_obj:
        filled += flow.path

    empties = []
    for spot in product(range(level_obj.size), repeat=2):
        if spot not in filled:
            empties += [spot]

    areas = []
    while empties:
        area = [empties.pop()]
        for spot in area:
            for adj in level_obj.find_adjacent(spot):
                try:
                    area += [empties.pop(empties.index(adj))]
                except ValueError:
                    pass
        areas += [area]
    return areas




