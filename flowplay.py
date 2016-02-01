def blah():
    for x in range(6):
            for y in range(6):
                if y == 4:
                    return 'blah'
                print(x,y)



print(blah())