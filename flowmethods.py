
def make_flows(array):
    """
    Creates a Flow object for each node in a given seed array.
    :param array: list of strings array
    :return: Flow objects
    """
    out = []
    node_set = lambda x: set([c for row in x for c in row if c])
    for node in node_set(array):
        helper = [node]
        for i, r in enumerate(array):
            for j, c in enumerate(r):
                if c == node:
                    helper += [(i, j)]
        out += [helper]
    return [Flow(colour, flow_path, end_point) for colour, flow_path, end_point in out]


class Flow(object):

        def __init__(self, colour, flow_path, finish):
            self.colour = colour
            self.flow_path = [flow_path]
            self.finish = finish

        def add_dot(self, position):
            self.flow_path.append(position)

        def check_complete(self):
            """
            returns True if Flow is complete
            Does this by testing if end of flow path is next to self.finish"""
            return 1 == sum([abs(i - j) for i, j in zip(self.flow_path[-1], self.finish)])

        def find_empties(self, array, size=3):
            """
            return list of tuples giving empty spaces next to flow end. False if none
            """
            row, col = self.flow_path[-1]
            adj_rows = [(row + adj, col) for adj in (-1, 1) if 0 <= row + adj < size and not array[row + adj][col]]
            adj_cols = [(row, col + adj) for adj in (-1, 1) if 0 <= col + adj < size and not array[row][col + adj]]
            return adj_rows + adj_cols


def make_array(flow_list, size=3):
    """
    Creates an array based on colours, paths and end points. Allows checking which spots are empty etc
    :param flow_list: list of Flow objects
    :param size: array side length
    :return: list of strings array
    """
    out = [['' for _ in range(size)] for _ in range(size)]
    for flow in flow_list:
        for row, col in flow.flow_path:
            out[row][col] = flow.colour
        out[flow.finish[0]][flow.finish[1]] = flow.colour
    return out


def print_array(array):
    """
    Call to easily print progress of given array. Can use make_array to print updated array on the fly
    :param array: list of strings array
    :return: None
    """
    for row in array:
        print(row)
    print()


def find_empties(array, flow_list, size=3):
    """
    Orders each flow by the number of possible moves. ie:
    [[f1, [(1,0)],
     [f2, [(1, 0), (0, 1)],
     [f3, [(2, 3), (3, 2), (1, 2)]]
    This is where optimisation of choosing position will happen. ATM it is purely by number of possible options.
    :param flow_list: list of Flows
    :param size: side length of level
    :return: Returns a list of lists of flows and possible (empty) spots
    """
    empties = [[flow, flow.find_empties(array, size)] for flow in flow_list if flow.find_empties(array, size) and not flow.check_complete()]
    return sorted(empties, key=lambda x: len(x[1]))


def check_blocked(flow_list, array, size=3):
    return any([len(flow.find_empties(array, size)) == 0 and not flow.check_complete() for flow in flow_list])


def rank_options(array, flow_list, size):
    flow_options = find_empties(array, flow_list, size)
    # The following section seems to stop code from solving properly.
    # after 50k loops and 20seconds. Need to think why
    blocked = check_blocked(flow_list, array, size)     #<blocked also seems to cause it to fail at solving after 3.6m loops and 37 minutes
    if blocked:
        return False
    for flow, options in flow_options:
        if len(options) == 1:
            return [[flow, options]]
    return flow_options
