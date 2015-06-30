#
# a = [4, 4, 3]
# d = [6, 6, 6, 6, 9]
# b = [10, 2]
# c = [4, 5, 1]
#
#
# l = [a, d, b, c]
#
# print(l)
#
# for flow in l:
#     flow.sort()
#
# l.sort()
# l.sort(key=lambda x: len(x))
#
# print(l)


a = [[9,[1]], [8,[1, 2, 2]], [7,[3, 5, 5]]]


def test(x):
    return x

for options in a:
    options[1].sort(key=test)

#a.sort(key=lambda x: test(x[1]))
print(a)