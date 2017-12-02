#
#  Solution on 0 balls
#

from pprint import pprint
from functools import lru_cache

n, m, k = map(int, input().split())
colors = map(int, input().split())

hashes = []

stations = {}
root = {}

for i in range(1, n + 1):
    root[i] = [next(colors), []]

for i in range(1, m + 1):
    u1, u2 = map(int, input().split())
    root[u2][1].append(u1)
    root[u1][1].append(u2)


@lru_cache(maxsize=None)
def check(k, N):
    global root
    abc = root
    if N > 5:
        return (False, abc)
    for i in range(1, n + 1):
        if root[i][0] == -1:
            colors = set(range(1, k + 1))
            for col in root[i][1]:
                if col in colors:
                    colors.remove(col)

            if len(colors) == 0:
                return (False, abc)
            else:
                eset = []
                for col in colors:
                    root[i][0] = col
                    eset.append(check(k, N + 1))
                oks = True
                for elem in eset:
                    if elem[0]:
                        oks = False
                        root = elem[1]
                        break
                if oks:
                    return (False, abc)
    return (True, root)


yet = check(k, 0)
ok = yet[0]

if ok:
    print('Yes')
    for i in yet[1]:
        print(i, end=' ')

else:
    print('No')
