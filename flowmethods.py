from flowlevels import *


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

    def find_empties(self, lvl):
        """
        return list of tuples giving empty spaces next to flow end. False if none
        """
        if not self.complete():
            row, col = self.path[-1]
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
        return 1 == sum([abs(i - j) for i, j in zip(self.path[-1], self.pair.path[-1])])

    def blocked(self, lvl):
        """
        returns True if Flow is blocked > not complete and no move options
        Does this by testing if flow is incomplete and has no options on one or both ends """
        # l3x2 should break immediately because f1 is blocked in (0, 0)
        return not self.find_empties(lvl) and not self.complete()


class Level(object):

    def __init__(self, lvl):
        # maybe make it take in flow_list as a parameter so make_flows doesnt need to be called every time we init lvl
        self.flow_list = make_flows(lvl)
        self.size = len(lvl)

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
        return any(f.blocked(self) for f in self.flow_list)

    def make_choice(self):
        """
        Takes move_options to give False, 1 or more options.
        Important to return ALL options unless
        :return:
        """
        options = self.move_options()
        #for flow, option in options:
            #if len(option) == 1:
            #    return [[flow, option]]
        #      if two flow ends are against the edge of the map, with none blocking
            # fill in the spots between
            # How do I get it to place all these moves? do i need to bypass add_dot
            # Can I memoise the fact that I have tried this? To prevent infinite loop.

            # If a loop end is next to a corner, fill that spot, return only that dot move

        return options

    def move_options(self):
        """Only enters if no nodes are blocked and none have 1 option only.
        ie - multiple Flows have multiple options
        #need to remember to return all options if introducing preemptive moves
        """
        #l3x1 should not be looping since n(0,0) is blocked
        if not self.blocked():
            flow_options = [[f, f.find_empties(self)] for f in self.flow_list if f.find_empties(self)]
            flow_options = sorted(flow_options, key=lambda x: len(x[1]))
            return flow_options
        return []

    def complete(self):
        map_full = all(all(row) for row in self.make_array())
        flows_done = all(f.complete() for f in self.flow_list)
        return flows_done and map_full


####

test = Level(l31)