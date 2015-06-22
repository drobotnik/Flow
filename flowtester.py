from flowlevels import *
from flowmethods import *
from flowRun import *


lt41 = [['1', '1', '', ''],
        ['', '', '', ''],
        ['', '', '', '2'],
        ['1', '1', '1', '2']]


def custom_solve(flowlist, size):
    """
    Returns a Level object based on custom inputted list of list of paths
    eg. paths = [[[(0, 0), (0, 1)], [(3, 0), (3, 1), (3, 2)]],
                 [[(3, 3)], [(2, 3)]]]
    custom_solve(paths, 4)
    :param flowlist: List of lists of paired Flow objects
    :return: Level object
    """
    pairs = flowlist
    out = []
    for n, [a, b] in enumerate(pairs):
        out += [[Flow(str(n), a), Flow(str(n), b)]]
    for a, b in out:
        a.link(b)
        b.link(a)
    return Level(sum(out, []), size)

