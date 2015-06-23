from flowmethods import *
from flowlevels import *
from testlevels import *
from copy import deepcopy
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


def test(array, size=0):
    if len(array) == 2:
        array, size = array
    global loops
    then = time.time()
    seed = Level(array, size)
    print('\n*****Testing.    size: {} Layout:'.format(seed.size))
    print(seed, '\n')
    input('Continue')
    solution = solve(deepcopy(seed))
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
    input('Continue')


if __name__ == "__main__":
    # test(l31)
    # #test(l42)  # Bug on this one because flows are 'finished' before map is full
    # test(l43)
    # test(l44)
    # test(l61)
    # test(l62)
    # test(l71)
    # #test(l72) # struggles with this one. Do i need to code in something for if all but one are done? and there are empty spaces?
    # test(l81)
    # test(l91)
    # test(l101)
    test(l121)
    test(l141)

