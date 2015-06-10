from flowmethods import *
from flowlevels import *
import copy
import time


loops = 0
clock = time.time()
start_clock = time.time()
end_clock = time.time()


def timer():
        #Code just to check performance
    global loops, start_clock, end_clock
    loops += 1
    if loops % 10000 == 0:
        end_clock, start_clock = time.time(), end_clock
        print('{}s for last 0.01m loops. Total loops: {}m, Total time: {}mins'.format(round(end_clock - start_clock, 2),
                                                                                round(loops / 100000, 2),
                                                                                round((time.time() - clock) / 60, 2)))


def test(array):
    global loops
    then = time.time()
    seed = Level(array)
    print('\n*****Testing. Level size: {} Layout:'.format(seed.size))

    print(seed, '\n')
    solution = solve(copy.deepcopy(seed))
    loops = 'N/A'
    outparams = (round(time.time() - then, 3), loops)
    outtext = '{} found in: {}, Loops: {}'
    if solution:
        pass

        print(outtext.format('Solution!', *outparams))
        for row in solution:
            print(row)
    else:
        print(outtext.format('Unsolvable!', *outparams))
        print(seed)

#test(l31)
test(l43)
#test(l44)
# test(l43)
# test(l61)
# test(l62)
# test(l71)
# #test(l72) # struggles with this one. Do i need to code in something for if all but one are done? and there are empty spaces?
# test(l91)
# #test(l14)

