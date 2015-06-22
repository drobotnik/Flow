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
    :return: list of Flows [flowA, flowB, flowC...]
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


def make_level(flowlist):
    """
    Returns a Level object based on custom inputted list of list of paths
    eg. paths = [[[(0, 0), (0, 1)], [(3, 0), (3, 1), (3, 2)]],
                 [[(3, 3)], [(2, 3)]]]
    make_level(paths, 4)
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
    return sum(out, [])


class Flow(object):

    def __init__(self, colour, path, pair=[]):
        self.colour = colour
        self.pair = pair
        if type(path) == tuple:  # These tests are to check if the flows are being created organically or for testing purposes
            self.path = [path]
        elif type(path) == list:
            self.path = path

    def __str__(self):
        return "Flow: {} Path: {} - {}".format(self.colour, self.path, self.pair.path[::-1])

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
            return adj_rows + adj_cols
        return False

    def add_dot(self, position):
        self.path += [position]

    def complete(self):
        """
        returns True if Flow is complete
        Does this by testing if end of flow path is next to self.finish"""
        return measure_distance(self.path[-1], self.pair.path[-1]) == 1

    def blocked(self, lvl):
        """
        returns True if Flow is blocked > not complete and no move options
        Does this by testing if flow is incomplete and has no options on one or both ends """
        # l3x2 should break immediately because f1 is blocked in (0, 0)
        blocked = not(self.find_empties(lvl) or self.complete())
        return blocked


class Level(object):

    def __init__(self, lvl, size=0):
        """
        Takes either a level diagram (list of lists) or a list of Flow objects
        :param lvl: either a list of Flows or level diagram
        :param size:
        :return:
        """
        if type(lvl[0]) == list:
            self.flow_list = make_flows(lvl)
            self.size = len(lvl)
        elif type(lvl[0]) == Flow:
            self.flow_list = lvl
            self.size = size

    def __str__(self):
        """
        returns formatted level
        """
        return '\n'.join(str([(c or ' ') for c in r]) for r in self.make_array())

    def __iter__(self):
        for flow in self.flow_list:
            yield flow

    def inspect_flows(self):
        for flow in self.flow_list:
            print(flow)

    def make_array(self):
        out = [['' for _ in range(self.size)] for _ in range(self.size)]
        for flow in self.flow_list:
            for row, col in flow.path:
                out[row][col] = flow.colour
        return out

    def find_adjacent(self, position):
        row, col = position
        adj_rows = [(row + adj, col) for adj in (-1, 1) if 0 <= row + adj < self.size]
        adj_cols = [(row, col + adj) for adj in (-1, 1) if 0 <= col + adj < self.size]
        return adj_rows + adj_cols

    def blocked(self):
        """
        returns True if any of the flows in the level are blocked
        :return: bool
        """
        dead_end = any(f.blocked(self) for f in self.flow_list)
        # blocked if it is empty and has 0 empties and 0 flow ends
        knot = self.knot_checker()

        return dead_end

    def knot_checker(self):
        filled = []
        for flow in self.flow_list:
            filled += flow.path[:-1]
        unfilled = []
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in filled:
                    unfilled += [(r, c)]
        for empty in unfilled:
            adjacent = self.find_adjacent(empty)
            if all(adj in filled for adj in adjacent):
                return True
        return False

    def complete(self):
        map_full = all(all(row) for row in self.make_array())
        flows_done = all(f.complete() for f in self.flow_list)
        return flows_done and map_full

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

    def score_option(self, flow_option):
        """
        Takes as input a possible move and returns a score for how favourable it is
        0 is best
        :param flow_option: [<flow>, (tup)]
        :return: float
        """
        flow, move = flow_option
        score = 1
        pot_empties = len(flow.find_empties(self, move))
        pair_empties = len(flow.pair.find_empties(self, flow.pair.path[-1]))
        if pot_empties == 1:
            score *= 0.1  # This is a corner or tunnel <- must be filled. Problem is, two ends may make a 'corner'
        if pot_empties == 2:
            score *= 0.5  # this is an edge
        if pot_empties < 3 and pair_empties < 3:  # prioritise flows where both ends are against an edge or corner
            score *= 0.1

        dist = lambda f, m: measure_distance(f.pair.path[-1], m)  # Ranks options by how close they take flow to finish. choice between 2 moves from same flow will be dist +/- 2
        score *= dist(flow, move) / 10  # reduces weighting of distance
        print('final score', round(score, 2), flow.colour, move)
        return score


def measure_distance(pos_one, pos_two):
    return sum([abs(i - j) for i, j in zip(pos_one, pos_two)])


def make_move(branch, options, flow, move):
    if branch > 0:
        last_move = options[branch - 1][0]
        last_move.path.pop()
    print('placing', flow.colour, move)
    flow.add_dot(move)


def solve(level):
    options = level.rank_options()
    if level.complete():
        return level.make_array()
    elif options:
        for n, [flow, move] in enumerate(options):
            make_move(n, options, flow, move)
            print('DE', level.blocked(), 'KN', level.knot_checker())
            print(level, '\n')
            possible = solve(copy.deepcopy(level))
            if type(possible) == list:
                return possible




