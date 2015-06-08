from flowlevels import *
import copy


def get_colours_and_nodes(lvl):
    """
    Gets list of colours and node locations.
    Called once when making Flow objects
    :param lvl: list of strings
    :return:[[str, tup, tup],...]
    """
    out = []
    node_set = lambda x: set([c for row in x for c in row if c])
    for node in node_set(lvl):
        helper = [node]
        for i, r in enumerate(lvl):
            for j, c in enumerate(r):
                if c == node:
                    helper += [(i, j)]
        out += [helper]
    return out


def make_flows(lvl):
    """
    Called once when starting level.
    makes a list of paired flows.
    feeds into Level.__init__. Could possibly be merged when it joins
    :param lvl:
    :return:
    """
    flow_list = []
    helper = []
    for colo, start, end in get_colours_and_nodes(lvl):
        helper += [[Flow(colo, start), Flow(colo, end)]]
    for x, y in helper:
        y.link(x)
        x.link(y)
        flow_list += [x, y]
    return flow_list


class Flow(object):

    def __init__(self, colour, path, pair=[]):
        self.colour = colour
        self.path = [path]
        self.pair = pair

    def link(self, pair):
        self.pair = pair

    def find_empties(self, lvl, position=None):
        """
        return list of tuples giving empty spaces next to flow end. False if none
        """
        if position is None:
            position = self.path[-1]
        if not self.complete():
            row, col = position
            adj_rows = [(row + adj, col) for adj in (-1, 1) if 0 <= row + adj < lvl.size and not lvl.make_array()[row + adj][col]]
            adj_cols = [(row, col + adj) for adj in (-1, 1) if 0 <= col + adj < lvl.size and not lvl.make_array()[row][col + adj]]
            #print('find empties:', adj_rows + adj_cols)
            return adj_rows + adj_cols
        return False

    def add_dot(self, position):
        self.path += [position]

    def complete(self):
        """
        returns True if Flow is complete
        Does this by testing if end of flow path is next to self.finish"""
        return measure_distance(self.path[-1], self.pair.path[-1]) == 1
        #print('Flow: {} done!'.format(self.colour))


    def blocked(self, lvl):
        """
        returns True if Flow is blocked > not complete and no move options
        Does this by testing if flow is incomplete and has no options on one or both ends """
        # l3x2 should break immediately because f1 is blocked in (0, 0)
        blocked = not self.find_empties(lvl) and not self.complete()
        if blocked:
            pass
            #print(self.colour, ' is blocked!')
        return blocked


class Level(object):

    def __init__(self, lvl):
        # maybe make it take in flow_list as a parameter so make_flows doesnt need to be called every time we init lvl
        self.flow_list = make_flows(lvl)
        self.size = len(lvl)
        self.history = []

    def __str__(self):
        """
        returns formatted level
        """
        return '\n'.join(str([(c or ' ') for c in r]) for r in self.make_array())

    def make_array(self):
        out = [['' for _ in range(self.size)] for _ in range(self.size)]
        for flow in self.flow_list:
            for row, col in flow.path:
                out[row][col] = flow.colour
        return out

    def blocked(self):
        """
        returns True if any of the flows in the level are blocked
        :return: bool
        """
        blocked = any(f.blocked(self) for f in self.flow_list)
        if blocked:
            pass
            #print('Level has blockage')
        return blocked

    def rank_options(self):
        """
        Takes make_options to give False, 1 or more options.
        Important to return ALL options unless
        :return:
        """
        options = self.make_options()
        options = sorted(options, key=lambda x: len(x[1]))

        for flow, option in options:
            if len(option) == 1:
                for move in option:
                    return [[flow, move]]
        out = []
        for flow, option in options:
            for move in option:
                out += [[flow, move]]  # Unpack options
        out = sorted(out, key=self.score_option)
        return out

    def make_options(self):
        """Only enters if no nodes are blocked and none have 1 option only.
        ie - multiple Flows have multiple options
        #need to remember to return all options if introducing preemptive moves
        """
        #l3x1 should not be looping since n(0,0) is blocked
        if not self.blocked():
            flow_options = [[f, f.find_empties(self)] for f in self.flow_list if f.find_empties(self)]
            return flow_options
        return []

    def complete(self):
        map_full = all(all(row) for row in self.make_array())
        flows_done = all(f.complete() for f in self.flow_list)
        return flows_done and map_full

    def score_option(self, flow_option):
        """
        Takes as input a possible move and returns a score for how favourable it is
        0 is best, 1 is worst
        :param flow_option: [<flow>, (tup)]
        :return: float
        """
        flow = flow_option[0]
        move = flow_option[1]
        score = 1
        pot_empties = len(flow.find_empties(self, move))
        if pot_empties == 1:
            score *= 0  # This is a corner or tunnel <- must be filled
        if pot_empties == 2:
            score *= 0.5  # this is an edge

        dist = lambda x: measure_distance(x[0].pair.path[-1], x[1])  # Ranks options by how close they take flow to finidh
        score = score * dist(flow_option)
        return score


def measure_distance(pos_one, pos_two):
    return sum([abs(i - j) for i, j in zip(pos_one, pos_two)])


def make_move(i, options, flow, move):
    if i > 0:
        last_move = options[i - 1][0]
        last_move.path.pop()
    flow.add_dot(move)


def print_all_options(options):
    for n, [flow, move] in enumerate(options):
        print("distance {}, flow {}, position {}".format(measure_distance(move, flow.pair.path[-1]),
                                                         flow.colour,
                                                         move))


def solve(level, recursion_level):
    options = level.rank_options()
    if level.complete():
        return level.make_array()
    elif options:
        #print_all_options(options)
        for n, [flow, move] in enumerate(options):
            make_move(n, options, flow, move)
            #print(level, '\n')
            possible_solution = solve(copy.deepcopy(level), recursion_level + 1)
            if type(possible_solution) == list:
                return possible_solution
