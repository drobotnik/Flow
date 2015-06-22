from flowlevels import *
from flowmethods import *
from flowRun import *


lt41 = [['1', '1', '1', '1'],
        ['', '1', '1', '1'],
        ['', '', '', ''],
        ['1', '1', '1', '']]


def custom_solve():
    """
    Returns a Level object based on custom inputted Flow
    :return:
    """
    pairs = [[Flow('1', [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 2), (1, 1)]),
              Flow('1', [(3, 0), (3, 1), (3, 2)])]]
    for pair in pairs:
        pair[0].link(pair[1])
        pair[1].link(pair[0])
    return Level(lt41, pairs[0])

solve(custom_solve())