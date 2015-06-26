def gentest():
    options = [['a', (0, 0, 5)], ['b', (0, 0)], ['c', (1, 0)], ['d',(0, 0)]]
    for flow, option in options:
        print(flow)
        for thing in option:
            yield thing
        break


for _ in gentest():
    print(_)