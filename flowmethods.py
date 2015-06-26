from copy import deepcopy
from itertools import product, chain
from string import ascii_uppercase, ascii_lowercase


def get_nodes(lvl):
    """
    Gets list of node locations from level diagra,.
    Called once when making Flow objects
    :param lvl: list of list of strings
    :return:[[[tup], [tup]],...]
    """
    out = []
    node_set = lambda x: set([c for row in x for c in row if c])
    for node in node_set(lvl):
        helper = []
        for i, r in enumerate(lvl):
            for j, c in enumerate(r):
                if c == node:
                    helper += [[(i, j)]]
        out += [helper]
    return out


def make_flows(flow_path_lists):
    """
    Returns a list of flows based on list of list of paths
    eg. paths = [[[(0, 0), (0, 1)], [(3, 0), (3, 1), (3, 2)]],
                 [[(3, 3)], [(2, 3)]]]
    make_level(paths, 4)
    :param flow_path_lists: List of lists of paired Flow objects
    :return: Level object
    """
    out = []
    for n, [a, b] in enumerate(flow_path_lists, 65):
        # print(n, a, b)

        out += [[Flow(chr(n), a), Flow(chr(n), b)]]
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

    def __len__(self):
        return len(self.path)

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
            adj_rows = [(row + adj, col) for adj in (-1, 1)
                        if 0 <= row + adj < lvl.size and not lvl.make_array()[row + adj][col]]
            adj_cols = [(row, col + adj) for adj in (-1, 1)
                        if 0 <= col + adj < lvl.size and not lvl.make_array()[row][col + adj]]
            return adj_rows + adj_cols
        return False

    def add_dot(self, position):
        self.path += [position]

    def complete(self):
        """
        returns True if Flow is complete
        Does this by testing if end of flow path is next to self.finish"""
        return distance(self.path[-1], self.pair.path[-1]) == 1

    def blocked(self, lvl):
        """
        returns True if Flow is blocked > not complete and no move options
        Does this by testing if flow is incomplete and has no options on one or both ends """
        # l3x2 should break immediately because f1 is blocked in (0, 0)
        blocked = not (self.find_empties(lvl) or self.complete())
        return blocked


class Level(object):
    def __init__(self, lvl, size=0):
        """
        Takes either a level diagram (list of lists) or a list of flow paths
        :param lvl: either a list of Flows or level diagram
        :param size:
        :return:
        """
        if type(lvl[0][0]) == str:
            # Make Level from diagram. Size given from shape
            self.flow_list = make_flows(get_nodes(lvl))
            self.size = len(lvl)
        else:
            # Make Level from inputted flow paths. Size needs to be explicitly stated
            if len(lvl) == 2:
                lvl, size = lvl
            self.flow_list = make_flows(lvl)
            self.size = size

    def __str__(self):
        """
        returns formatted level
        """
        return '\n'.join(str([(c or ' ') for c in r]) for r in self.make_array())

    def __iter__(self):
        for flow in self.flow_list:
            yield flow

    def __len__(self):
        return self.size

    def make_array(self):
        out = [['' for _ in range(self.size)] for _ in range(self.size)]
        for flow in self.flow_list:
            for row, col in flow.path:
                if (row, col) == flow.path[-1]:
                    out[row][col] = chr(ord(flow.colour) + 32)
                else:
                    out[row][col] = flow.colour
        return out

    def adjacent_types(self, position):
        empties, tube, ends = [], [], []
        for r, c in self.find_adjacent(position):
            if self.make_array()[r][c] in ascii_lowercase:
                ends += [(r, c)]
            elif not self.make_array()[r][c]:
                empties += [(r, c)]
            elif self.make_array()[r][c] in ascii_uppercase:
                tube += [(r, c)]
            else:
                raise Exception("position{} pos{} adj{} emp{} "
                                "tub{} end{}".format(position, (r, c), self.find_adjacent(position), empties, tube, ends))
        return empties, tube, ends

    def complete(self):
        map_full = all(all(row) for row in self.make_array())
        flows_done = all(f.complete() for f in self.flow_list)
        return flows_done and map_full

    def make_options(self):
        """Only enters if no nodes are blocked and none have 1 option only.
        ie - multiple Flows have multiple options
        #need to remember to return all options if introducing preemptive moves
        """
        if any(self.impossibilities()):
            return []
        else:
            flow_options = ([f, f.find_empties(self)] for f in self.flow_list if f.find_empties(self))
            # flow_options = [[f, f.find_empties(self)] for f in self.flow_list if f.find_empties(self)]
            return flow_options

    def rank_options(self):
        """
        Takes make_options to give False, 1 or more options.
        Important to return ALL options unless
        :return:
        """
        options = list(self.make_options())
        options = sorted(options, key=lambda x: len(x[1]))
        for flow, option in options:
            for move in sorted(option, key=self.score_option):
                yield [flow, move]  # Unpack options
            break

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

        dist = lambda f, m: distance(f.pair.path[-1],
                                     m)  # Ranks options by how close they take flow to finish. choice between 2 moves from same flow will be dist +/- 2
        score *= dist(flow, move) / 10  # reduces weighting of distance
        # print('final score', round(score, 2), flow.colour, move)
        return score

    def area_finder(self):
        """
        Returns the different areas
        This is to make it easier to test if the ends are in the areas
        :return: list of tuples
        """
        empties = list(chain(*([(r, c)] for r, c in product(range(self.size), repeat=2) if not self.make_array()[r][c])))
        areas = []
        while empties:
            area = [empties.pop()]
            for spot in area:
                for adj in self.find_adjacent(spot):
                    try:
                        area += [empties.pop(empties.index(adj))]
                    except ValueError:
                        pass
            areas += [area]
        ends = [flow.path[-1] for flow in self]
        for end in ends:
            for area in areas:
                for pos in self.find_adjacent(end):
                    if pos in area:
                        area += [end]
                        break
        return areas

    def blocked(self):
        """
        returns True if any of the flows in the level are blocked
        :return: bool
        """
        return any(f.blocked(self) for f in self.flow_list)
        # blocked if it is empty and has 0 empties and 0 flow ends

    def seperated_flows(self):
        """
        Return True if not all Flow ends are in the same 'area' ie possible to be connected
        :return: bool
        """
        connected_flows = 0
        for flow in self:
            if flow.complete():
                connected_flows += 1
            else:
                for area in self.area_finder():
                    if (flow.path[-1] in area) and (flow.pair.path[-1] in area):
                        connected_flows += 1
                        break
        return connected_flows != len(self.flow_list)

    def dammed(self):
        """
        Returns True if any areas are isolated ie have no (incomplete) Flow ends in them
        Gets all areas to see if they have at least one flow end in it
        If any dont have a Flow end then it returns True
        usage: if not Level.dammed(): continue
        :return: bool
        """
        total = 0
        for area in self.area_finder():
            for flow in self:
                if (flow.path[-1] in area) and (flow.pair.path[-1] in area) and not flow.complete():
                    total += 1
                    break
        return total != len(self.area_finder())

    def find_adjacent(self, position, diag=False):
        row, col = position
        if not diag:
            adj_rows = [(row + adj, col) for adj in (-1, 1) if 0 <= row + adj < self.size]
            adj_cols = [(row, col + adj) for adj in (-1, 1) if 0 <= col + adj < self.size]
            return adj_rows + adj_cols
        elif diag:
            out = []
            for r, c in product(range(-1, 2), repeat=2):
                if 0 not in (r, c):
                    if all(0 <= index < self.size for index in (row + r, col + c)):
                        out += [(row + r, col + c)]
            adj_rows = [(row + adj, col) for adj in (-2, 2) if 0 <= row + adj < self.size]
            adj_cols = [(row, col + adj) for adj in (-2, 2) if 0 <= col + adj < self.size]
            out += adj_rows + adj_cols
            return out

    def cornered(self, specific=False):
        """
        States whether there is at least one cornered spot or not.
        Takes optional parameter of a position.
        Says if the areas AROUND that position are cornered or not (exluding position). (based on behaviour of find_adjacent)
        It is important this check is done just after placing to ensure any corners are caught.
        Without optional param, scans all empty spots in Level
        :param position: tup(int, int)
        :return: bool
        """
        if type(specific) == tuple:
            #ends = [specific]
            raise Exception('Im assuming this section is only for testing')
        else:
            # print('inspecific')
            ends = (flow.path[-1] for flow in self if not flow.complete())
            #print('ends', ends)
        for end in ends:  # for each end
            for r, c in self.find_adjacent(end, diag=True):  # for each 'danger square'
                #print(end, 'pos', position)
                if not self.make_array()[r][c]:
                    safe_spaces = 0  # count safe spaces
                    for ar, ac in self.find_adjacent((r, c), diag=False):  # for each space next to danger square
                        #print('end', end, 'pos', position, 'space', space)
                        if self.make_array()[ar][ac] in ascii_lowercase or not self.make_array()[ar][ac]:  # if safe
                            safe_spaces += 1  # if record so
                            #print(safe_spaces)
                            if safe_spaces > 1:
                                break
                    else:
                        print('cornered', 'end', end, 'pos', (r, c))
                        print(self)
                        print(_)
                        return True
        return False

    def impossibilities(self):
        yield self.blocked()
        yield self.seperated_flows()
        yield self.dammed()
        yield self.cornered()




def distance(pos_one, pos_two):
    return sum(abs(i - j) for i, j in zip(pos_one, pos_two))


def make_move(branch, options, flow, move):
    if branch > 0:
        last_move = options[branch - 1][0]
        last_move.path.pop()
    flow.add_dot(move)


def solve(level):
    print(level, '\n')
    options = level.rank_options()
    if level.complete():
        return level.make_array()
    elif options:
        for n, [flow, move] in enumerate(options):
            make_move(n, options, flow, move)
            possible = solve(deepcopy(level))
            if type(possible) == list:
                return possible




