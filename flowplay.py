def test():
    a = [0, 0, 1, 0]
    b = [1, 1]
    c = [0, 1, 1]
    d = [0, 0, 0, 1]

    for i in [a, b, c, d]:
        safe = 0
        for n in i:
            if n:
                safe += 1
                if safe > 1:
                    break
        else:
            print(i)
            return True
    return False

print(test())
