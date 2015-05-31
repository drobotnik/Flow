from flowmethods import *
from flowlevels import *
import copy
import time



loops = 0
clock = time.time()
start_clock = time.time()
end_clock = time.time() - start_clock


def solve(flow_list, size, recursion_level):
    global loops, start_clock, end_clock
    loops += 1
    array = make_array(flow_list, size)
    if loops % 100000 == 0:
        end_clock, start_clock = time.time(), end_clock
        print('{}s for last 0.1m loops. Total loops: {}m, Total time: {}mins'.format(round(end_clock - start_clock, 2),
                                                                                round(loops / 1000000, 2),
                                                                                round((time.time() - clock) / 60, 2)))
    full_board = all(all(row) for row in make_array(flow_list, size))
    all_complete = all(flow.check_complete() for flow in flow_list)
    move_options = rank_options(array, flow_list, size)
    if all_complete and full_board:
        return make_array(flow_list, size)
    elif move_options:
        for flow, moves in move_options:
            for move in moves:
                flow.add_dot(move)
                possible_solution = solve(copy.deepcopy(flow_list), size, recursion_level + 1)
                if type(possible_solution) == list:
                    return possible_solution


def test(array, tsize):
    print('Testing:')
    global loops
    then = time.time()
    seed = make_flows(array)
    solution = solve(copy.deepcopy(seed), tsize, 0)
    if solution:
        print('SOLUTION found in: {}, Loops: {}'.format(str(time.time() - then), str(loops)))
        print_array(make_array(seed, tsize))
        loops = 0
        print_array(solution)
    else:
        print('UNSOLVABLE: {}, Loops: {}'.format(str(time.time() - then), str(loops)))
        print_array(make_array(seed, tsize))
        loops = 0


test(l31, 3)
test(l3x2, 3)
test(l44, 4)
test(l43, 4)
test(l51, 5)
test(l52, 5)
test(l61, 6)
test(l62, 6)
test(l71, 7)
test(l72, 7)
test(l91, 9)

