from flowMethods2 import *
from flowlevels import *
import copy
import time


loops = 0
clock = time.time()
start_clock = time.time()
end_clock = time.time()




def solve(level, recursion_level):
    #Code just to check performance
    global loops, start_clock, end_clock
    loops += 1
    if loops % 10000 == 0:
        end_clock, start_clock = time.time(), end_clock
        print('{}s for last 0.01m loops. Total loops: {}m, Total time: {}mins'.format(round(end_clock - start_clock, 2),
                                                                                round(loops / 100000, 2),
                                                                                round((time.time() - clock) / 60, 2)))
    #Actual code below
    if level.complete():
        return level.make_array()
    elif level.make_choice():
        for flow, moves in level.make_choice():
            for move in moves:
                flow.add_dot(move)
                possible_solution = solve(copy.deepcopy(level), recursion_level + 1)
                if type(possible_solution) == list:
                    return possible_solution




def test(array):
    global loops
    then = time.time()
    print('\n***** Testing:')
    seed = Level(array)
    print(seed, '\n')
    solution = solve(copy.deepcopy(seed), 0)
    outparams = (round(time.time() - then, 3), loops, seed.size)
    outtext = '{} found in: {}, Loops: {}, Size: {}'
    if solution:

        print(outtext.format('Solution!', *outparams))
        for row in solution:
            print(row)
    else:
        print(outtext.format('Unsolvable!', *outparams))


test(l31)

test(l3x2)

test(l44)

test(l43)
test(l51)

test(l52)

test(l61)

test(l62)  #still same bug where it fails to solve this one

# test(l71)

# test(l72)

# test(l91)

###