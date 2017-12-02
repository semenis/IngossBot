#
# Solution on 100 balls
#

from functools import lru_cache

n, k, s, x = map(int, input().split())

root = []


@lru_cache(maxsize=None)
def count(n, k, s):
    return s + k - n * ((s + k) // n)


ans = -1

for i in range(n):
    s = count(n, k, s)
    root.append(s)
    inx = root.__len__() // 2
    if root[-1] == x:
        ans = len(root)
        break
    if root[:inx] == root[inx:]:
        break

print(ans)
