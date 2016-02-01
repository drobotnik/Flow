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
        if type(
                path) == tuple:  # These tests are to check if the flows are being created organically or for testing purposes
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
        if blocked:
            print('blocked!!')
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
            else:
                raise Exception('Where is this Level being created? needs Size')
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
                if (row, col) != flow.path[-1]:
                    out[row][col] = flow.colour
                else:
                    out[row][col] = chr(ord(flow.colour) + 32)
        return out

    def adjacent_types(self, position):
        empties, tube, ends = [], [], []
        for r, c in self.find_adjacent(position):
            if not self.make_array()[r][c]:
                empties += [(r, c)]
            elif self.make_array()[r][c] in ascii_uppercase:
                tube += [(r, c)]
            elif self.make_array()[r][c] in ascii_lowercase:
                ends += [(r, c)]
            else:
                raise Exception("position{} pos{} adj{} emp{} "
                                "tub{} end{}".format(position, (r, c), self.find_adjacent(position), empties, tube,
                                                     ends))
        return empties, tube, ends

    def complete(self):
        # map_full = all(all(row) for row in self.make_array())
        flows_done = all(f.complete() for f in self.flow_list)
        return flows_done  # and map_full

    def make_options(self):
        """
        1. First checks self.impossibilities() to see if Level is solvable or not.
        2. Then makes flow_options which is all the empty spots next to all incomplete Flow ends
        3. returns rejigged flow_options

        :return: [[Flow1, [option1, option2],...]
        or       [[option1, [Flow1, Flow2],...]
        """
        if any(self.impossibilities()):
            input('impossible*:\n{}\n\n'.format(self))

            return []
        flow_options = ([f, f.find_empties(self)] for f in self.flow_list if f.find_empties(self))
        out = []
        for flow, option in flow_options:  # first check to filter out any corners
            if len(option) == 1:  # returns any Flow with only one option
                return [[flow, option]]
            out += [[flow, option]]
        return self.rejigger(out)

    def rejigger(self, flow_options):
        """
        Takes as input a set of Flow options, checks if there are any corners and rejigs if there are.
        Also checks if any Flows have only one option, and prioritises returning that

        :param flow_options: [[Flow1, [option1, option2],...]
        :return: [[Flow1, [option1, option2],...]
        or       [[option1, [Flow1, Flow2],...]
        """
        cornered = {}
        for flow, option in flow_options:  # first check to filter out any corners
            if len(option) == 1:  # returns any Flow with only one option
                return [[flow, option]]
            for move in option:  # checks all moves
                if self.cornered(move):  # if any potential moves are a corner
                    try:
                        cornered[move] += [flow]
                    except KeyError:
                        cornered[move] = []
                        cornered[move] += [flow]
        if cornered:  # if any corners
            out = []
            for key in cornered:
                if len(cornered[key]) == 1:  # if any cornered squares have only one end next to it
                    return [[cornered[key][0], [key]]]  # return just that move in unregigged format
                else:
                    out += [[key, cornered[key]]]
            return out
        elif not cornered:
            return flow_options
        else:
            raise Exception('Something weird has happened in rejigger')

    def rank_options(self):
        """
        Takes make_options to give False, 1 or more options.
        Important to return ALL options unless
        :yield: option
        """
        options = self.make_options()
        #print('ops:')

        if options:
            if isinstance(options[0][0], tuple):
                # print('rejigged...')
                for move, flows in options:
                    #print(move, [flow.colour for flow in flows])
                    for flow in flows:
                        yield [flow, move]
                    break
            elif isinstance(options[0][0], Flow):
                #print('original')
                if len(options) > 1:
                    for flow, moves in options:
                        moves.sort(key=lambda x: self.score_option((flow, x)))  # ranks options within flow
                    options.sort(key=lambda x: self.score_option((x[0], x[1][0])))  # ranks flows by best option
                    options.sort(key=lambda x: len(x[0]))  # ranks options by length of flow
                    options.sort(key=lambda x: len(x[1]))  # ranks flows by number of options  ** note could use this to speed up above. if any flows have one option, return that one, if any have 2 return those 2 only. then no need to sort them all multiple times
                for flow, moves in options:
                    for move in moves:
                        yield [flow, move]  # Unpack options
                    break

    def score_option(self, flow_option):
        """
        Takes as input a possible move and returns a score for how favourable it is
        0 < score
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

    def find_empties(self):
        all_grid_options = product(range(self.size), repeat=2)
        level = self.make_array()
        return list((r, c) for r, c in all_grid_options if not level[r][c])

    def area_separator(self, empties):
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
        return areas

    def add_ends_to_areas(self, areas):
        ends = [flow.path[-1] for flow in self]
        for end in ends:
            for area in areas:
                for pos in self.find_adjacent(end):
                    if pos in area:
                        area += [end]
                        break
        return areas

    def area_finder(self):
        """
        Returns the different areas
        This is to make it easier to test if the ends are in the areas
        :return: list of tuples
        """
        empties = self.find_empties()
        areas = self.area_separator(empties)
        areas = self.add_ends_to_areas(areas)
        return areas

    def blocked(self):
        """
        returns True if any of the flows in the level are blocked
        :return: bool
        """
        return any(f.blocked(self) for f in self.flow_list)
        # blocked if it is empty and has 0 empties and 0 flow ends

    def separated_flows(self):
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
        separated = connected_flows != len(self.flow_list)
        if separated:
            print('separated', connected_flows, len(self.flow_list))
        return separated

    def dammed(self):
        """
        Returns True if any areas are isolated ie have no (incomplete) Flow pair ends in them
        Gets all areas to see if they have at least one flow end in it
        If any don't have a Flow end then it returns True
        usage: if not Level.dammed(): continue
        :return: bool
        """
        total = 0
        for area in self.area_finder():
            for flow in self:
                if (flow.path[-1] in area) and (flow.pair.path[-1] in area) and not flow.complete():
                    total += 1
                    break
        dammed = total != len(self.area_finder())
        if dammed:
            print('dammed')
        return dammed

    def find_adjacent(self, position):
        row, col = position
        adj_rows = [(row + adj, col) for adj in (-1, 1) if 0 <= row + adj < self.size]
        adj_cols = [(row, col + adj) for adj in (-1, 1) if 0 <= col + adj < self.size]
        return adj_rows + adj_cols

    def cornered(self, pos):
        """
        checks a position to see if it is cornered: defined as having only one empty space next to it
        :param pos: tuple coordinate
        :return: bool
        """
        if self.make_array()[pos[0]][pos[1]]:
            # raise ValueError('Cornered check found spot {} to not be empty'.format(pos))
            pass
        safe_spaces = 0  # count safe spaces
        for ar, ac in self.find_adjacent(pos):  # for each space next to pos
            if not self.make_array()[ar][ac]:  # if empty..
                safe_spaces += 1  # record so
                if safe_spaces > 1:
                    break
        else:
            return True
        return False

    def folded(self):
        """
        Checks to see if any flows are folded over themselves
        :return: bool
        """
        level = self.make_array()
        for i in range(len(level) - 1):
            for j in range(len(level) - 1):
                if level[i][j]:
                    colour = (level[i][j].upper(), level[i][j].lower())
                    if level[i + 1][j + 1] in colour:  # start with least likely
                        if level[i][j + 1] in colour:
                            if level[i + 1][j] in colour:
                                print('folded')
                                return True
        return False

    def impossibilities(self):
        # yield self.blocked()
        # yield self.folded()
        # yield self.dammed()
        yield self.separated_flows()


def distance(pos_one, pos_two):
    return sum(abs(i - j) for i, j in zip(pos_one, pos_two))


def solve(level):
    print(level, '\n')
    options = level.rank_options()
    if level.complete():
        return level.make_array()
    elif options:
        last = 0
        for flow, move in options:
            if last:
                last.path.pop()
            last = flow
            flow.add_dot(move)
            possible = solve(deepcopy(level))
            if type(possible) == list:
                return possible