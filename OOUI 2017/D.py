#
#  Solution on 71 balls
#

from functools import lru_cache

n, k = map(int, input().split())
s = input()

root = list(map(lambda x: (x, x+1), range(k)))
root[-1] = (root[-1][0], len(s))
root = [s[I[0]:I[1]] for I in root]

@lru_cache(maxsize=None)
def check(s):
    return str(s) == str(int(s))

def ls(root):
    return any(map(lambda x: check(x), root))

ans = []

for i in range(root.__len__()-1, 0, -1):
    while len(root[i])-1:
        if ls(root): ans.append(sum(map(int, root)))

        hs = root[i][0]
        root[i] = root[i][1:]
        root[i - 1] = root[i - 1] + hs

if ls(root): ans.append(sum(map(int, root)))

print(max(ans))
