from flowmethods import *
from flowlevels import *
from testlevels import *
from copy import deepcopy
import time
import cProfile


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
    if len(array) == 2:
        array, size = array
    global loops
    then = time.time()
    seed = Level(array)
    print('\n*****Testing.    size: {}'.format(seed.size))
    #print(seed, '\n')
    #input('Continue')
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
        #input('fail')
    #input('Continue')


if __name__ == "__main__":
    levels = [
              # l31,
              # l42,  # Bug on this one because flows are 'finished' before map is full
              # l43,
              # l44,#,
              # l51,
              # l61,
              # l62,
              # l71,
              # # l72,  # struggles with this one. Do i need to code in something for if all but one are done? and there are empty spaces?
              l81
              # l91,
              # l101,
              # l111,
              # l121,
    #          l141
    ]

    for n, level in enumerate(levels):
        test(level)
    # cProfile.run("solve(Level(l31))")



